"""
DataHub — FastAPI backend.
- JWT auth (python-jose + passlib pbkdf2_sha256)
- WebSocket proxy do Streamlit
- HTTP proxy do Streamlit
- Vue.js SPA frontend (static)
- REST API dla APEX, AI, DDT
"""

# ===========================================================================
# Imports
# ===========================================================================

import asyncio
import atexit
import os
import pathlib
import random
import signal
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional

import aiohttp
import websocket as ws_client
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# ===========================================================================
# Version
# ===========================================================================

APP_VERSION = "v0.7.0"

# ===========================================================================
# JWT Config
# ===========================================================================

SECRET_KEY = os.getenv("JWT_SECRET", os.urandom(32).hex())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8h

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# ===========================================================================
# DB
# ===========================================================================

DB_URL = os.getenv("DATABASE_URL") or "sqlite:///users.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)


Base.metadata.create_all(bind=engine)

# ===========================================================================
# Pydantic schemas
# ===========================================================================


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    username: str
    role: str = "Developer"
    initials: str


# ===========================================================================
# Auth helpers
# ===========================================================================


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def _compute_initials(username: str) -> str:
    parts = username.replace(".", " ").split()
    return "".join(p[0].upper() for p in parts if p)[:2]


def _get_user_from_db(username: str) -> Optional[User]:
    db = SessionLocal()
    try:
        return db.query(User).filter_by(username=username).first()
    finally:
        db.close()


def _create_user(username: str, password: str) -> User:
    db = SessionLocal()
    try:
        user = User(username=username, password_hash=_hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


# ===========================================================================
# Seed domyślnego użytkownika
# ===========================================================================

db_session = SessionLocal()
try:
    existing = db_session.query(User).filter_by(username="admin").first()
    if not existing:
        admin = User(username="admin", password_hash=_hash_password("admin123"))
        db_session.add(admin)
        db_session.commit()
        print("Utworzono domyślnego użytkownika: admin / admin123")
except IntegrityError:
    db_session.rollback()
finally:
    db_session.close()

# ===========================================================================
# Streamlit subprocess management
# ===========================================================================

STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
STREAMLIT_BASE = f"http://localhost:{STREAMLIT_PORT}"
STREAMLIT_WS_BASE = f"ws://localhost:{STREAMLIT_PORT}"

_streamlit_process = None
_STREAMLIT_PIDFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit.pid")


def _start_streamlit():
    """Uruchamia Streamlit jako subproces OS."""
    global _streamlit_process
    if _is_streamlit_alive():
        print(f"[streamlit] Already running on port {STREAMLIT_PORT}")
        return

    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "streamlit_app.py")
    cmd = [
        sys.executable, "-m", "streamlit", "run", script,
        "--server.port", str(STREAMLIT_PORT),
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.enableWebsocketCompression", "false",
        "--server.baseUrlPath=streamlit",
        "--browser.gatherUsageStats", "false",
    ]
    try:
        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True

        _streamlit_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)
        with open(_STREAMLIT_PIDFILE, "w") as f:
            f.write(str(_streamlit_process.pid))
        print(f"[streamlit] PID {_streamlit_process.pid} on port {STREAMLIT_PORT}")

        time.sleep(2)
        if _streamlit_process.poll() is not None:
            print(f"[streamlit] WARNING — died immediately (code {_streamlit_process.returncode})")
        else:
            print("[streamlit] Started successfully")
    except Exception as e:
        print(f"[streamlit] ERROR — {e}")


def _is_streamlit_alive():
    if _streamlit_process is not None and _streamlit_process.poll() is None:
        return True
    pidfile = pathlib.Path(_STREAMLIT_PIDFILE)
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            pidfile.unlink(missing_ok=True)
    return False


def _stop_streamlit():
    global _streamlit_process
    if _streamlit_process is not None and _streamlit_process.poll() is None:
        print("[streamlit] Stopping…")
        try:
            if sys.platform == "win32":
                _streamlit_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                _streamlit_process.terminate()
            _streamlit_process.wait(timeout=5)
        except Exception:
            _streamlit_process.kill()
            _streamlit_process.wait()
        print("[streamlit] Stopped")
    pathlib.Path(_STREAMLIT_PIDFILE).unlink(missing_ok=True)


atexit.register(_stop_streamlit)

# ===========================================================================
# FastAPI app
# ===========================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start Streamlit przy starcie, stop przy shutdownie."""
    _start_streamlit()
    yield
    _stop_streamlit()


app = FastAPI(title="DataHub API", version=APP_VERSION, lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================================
# Auth dependency
# ===========================================================================


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Zwraca payload JWT lub rzuca 401."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _decode_token(credentials.credentials)


# ===========================================================================
# API routes — Auth
# ===========================================================================


@app.post("/api/login", response_model=TokenResponse)
def login(body: LoginRequest):
    username = body.username.strip()
    user = _get_user_from_db(username)
    if not user or not _verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Niepoprawna nazwa użytkownika lub hasło")

    token = _create_access_token({"sub": user.username, "id": user.id})
    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "role": "Developer",
            "initials": _compute_initials(user.username),
        },
    )


@app.post("/api/register", status_code=201)
def register(body: RegisterRequest):
    username = body.username.strip()
    if not username or not body.password:
        raise HTTPException(status_code=400, detail="Uzupełnij wszystkie pola")

    existing = _get_user_from_db(username)
    if existing:
        raise HTTPException(status_code=409, detail="Użytkownik już istnieje")

    _create_user(username, body.password)
    return {"ok": True}


@app.post("/api/logout")
def logout():
    """JWT jest bezstanowy — klient usuwa token po swojej stronie."""
    return {"ok": True}


@app.get("/api/me")
def me(payload: dict = Depends(get_current_user)):
    username = payload.get("sub")
    user_id = payload.get("id")
    return {
        "id": user_id,
        "username": username,
        "role": "Developer",
        "initials": _compute_initials(username),
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "DataHub API", "version": APP_VERSION}


# ===========================================================================
# API routes — APEX (mock)
# ===========================================================================


def _apex_kpi():
    return {
        "uptime": round(98 + random.random() * 1.9, 1),
        "uptime_trend": random.choice(["up", "down"]),
        "uptime_change": round(random.uniform(0.1, 0.5), 1),
        "transactions": random.randint(1000, 3000),
        "transactions_trend": random.choice(["up", "down"]),
        "transactions_change": random.randint(5, 20),
        "avg_processing_sec": random.randint(30, 90),
        "avg_processing_trend": random.choice(["up", "down"]),
        "avg_processing_change": random.randint(1, 10),
        "sla": round(98 + random.random() * 1.9, 1),
        "sla_trend": random.choice(["up", "down"]),
        "sla_change": round(random.uniform(0.1, 0.3), 1),
        "timestamp": datetime.now().isoformat(),
    }


def _apex_trends():
    months = ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip"]
    return [{"month": m, "transactions": random.randint(800, 3500), "errors": random.randint(5, 50)} for m in months]


def _apex_reports():
    statuses = ["ready", "ready", "ready", "generating"]
    names = [
        "Raport_dzienny_KPI", "SLA_Compliance_Q2", "ETL_Performance_Weekly",
        "Data_Quality_Scorecard", "Capacity_Forecast_Q3", "Error_Analysis",
        "Cost_Tracker_MTD", "User_Activity_Report",
    ]
    authors = ["B. Gawron", "A. Kowalski", "K. Nowak", "System"]
    return [
        {
            "id": i + 1,
            "name": random.choice(names) + "_" + datetime.now().strftime("%Y-%m-%d") + random.choice([".pdf", ".xlsx", ".html"]),
            "size": f"{random.randint(200, 5000)} KB",
            "date": (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
            "author": random.choice(authors),
            "status": random.choice(statuses),
        }
        for i in range(8)
    ]


def _apex_etl():
    workflows = ["LOAD_CUSTOMER", "LOAD_TRANSACTIONS", "SYNC_ACCOUNTS", "CALC_INTEREST", "GEN_REPORT", "AGG_DAILY_KPI"]
    return [
        {
            "workflow": wf,
            "avg_duration_min": random.randint(5, 45),
            "rows_processed": random.randint(10000, 5000000),
            "success_rate": round(90 + random.random() * 10, 1),
            "status": random.choice(["stable", "stable", "stable", "degraded"]),
        }
        for wf in workflows
    ]


def _apex_sla():
    services = ["ETL Pipeline", "API Gateway", "Database OLTP", "Reporting DB", "Authentication"]
    return [
        {
            "service": svc,
            "sla_target": 99.5,
            "actual": round(98 + random.random() * 2, 2),
            "incidents": random.randint(0, 5),
            "status": "ok" if random.random() > 0.3 else "warning",
        }
        for svc in services
    ]


def _apex_alerts():
    levels = ["critical", "warning", "info"]
    sources = ["PowerCenter", "TeamCity", "Oracle", "Snowflake", "App Server"]
    messages = [
        "Connection pool exhausted", "Table space > 85%",
        "Build failed: payment-gateway", "ETL workflow aborted",
        "Long running query detected", "Certificate expires in 7 days",
    ]
    return [
        {
            "id": i + 1,
            "level": random.choice(levels),
            "source": random.choice(sources),
            "message": random.choice(messages),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
        }
        for i in range(6)
    ]


@app.get("/api/apex/kpi")
def apex_kpi():
    return {"success": True, "data": _apex_kpi()}


@app.get("/api/apex/trends")
def apex_trends():
    return {"success": True, "data": _apex_trends()}


@app.get("/api/apex/reports")
def apex_reports():
    return {"success": True, "data": _apex_reports()}


@app.get("/api/apex/etl")
def apex_etl():
    return {"success": True, "data": _apex_etl()}


@app.get("/api/apex/sla")
def apex_sla():
    return {"success": True, "data": _apex_sla()}


@app.get("/api/apex/alerts")
def apex_alerts():
    return {"success": True, "data": _apex_alerts()}


# ===========================================================================
# Streamlit — HTTP proxy (aiohttp zamiast httpx — stabilniejszy streaming)
# ===========================================================================

@app.api_route("/streamlit/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@app.api_route("/streamlit/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def streamlit_http_proxy(request: Request, path: str = ""):
    """Proxy HTTP dla Streamlit przez aiohttp."""
    target_url = f"{STREAMLIT_BASE}/streamlit/{path}"
    try:
        body = await request.body()
        async with aiohttp.ClientSession() as session:
            headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host",)}
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
            ) as resp:
                excluded = {"content-encoding", "transfer-encoding", "connection", "content-length", "server"}
                out_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}

                # Czytamy całe body (pliki JS/CSS są małe, strona Streamlit też)
                content = await resp.read()

        return Response(
            content=content,
            status_code=resp.status,
            headers=out_headers,
        )
    except aiohttp.ClientConnectorError:
        print(f"[streamlit] Connect error: {target_url}")
        return JSONResponse({"error": "Streamlit nie jest dostępny"}, status_code=502)
    except Exception as e:
        import traceback
        print(f"[streamlit] Proxy error: {type(e).__name__}: {e}")
        traceback.print_exc()
        return JSONResponse({"error": f"Streamlit proxy error: {type(e).__name__}"}, status_code=502)


# ===========================================================================
# Streamlit — WebSocket proxy (aiohttp, pełna diagnostyka)
# ===========================================================================


@app.websocket("/_stcore/{path:path}")
@app.websocket("/streamlit/_stcore/{path:path}")
async def streamlit_ws_proxy(websocket: WebSocket, path: str):
    """Proxy WebSocket do Streamlit przez aiohttp."""
    # Wybierz sub-protokół z nagłówka przeglądarki (np. "streamlit")
    subprotocols = websocket.headers.get("sec-websocket-protocol", "")
    selected = subprotocols.split(",")[0].strip() if subprotocols else None
    print(f"[ws] Sub-protocol offered: {subprotocols!r}  selected: {selected!r}")
    await websocket.accept(subprotocol=selected)

    target_url = f"ws://localhost:{STREAMLIT_PORT}/streamlit/_stcore/{path}"
    headers = {k: v for k, v in websocket.headers.items()
               if k.lower() in ("origin", "cookie", "sec-websocket-protocol") and v}
    print(f"[ws] New connection → {target_url}  headers={headers}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(target_url, timeout=5.0, headers=headers or None) as ws:
                print(f"[ws] Connected to Streamlit")

                async def relay_to_client():
                    """Streamlit → Client."""
                    try:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                print(f"[ws] → text ({len(msg.data)} chars)")
                                await websocket.send_text(msg.data)
                            elif msg.type == aiohttp.WSMsgType.BINARY:
                                print(f"[ws] → binary ({len(msg.data)} bytes)")
                                await websocket.send_bytes(msg.data)
                            elif msg.type == aiohttp.WSMsgType.CLOSED:
                                print(f"[ws] ← Streamlit closed")
                                break
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                print(f"[ws] ← Streamlit error")
                                break
                    except Exception as e:
                        print(f"[ws] relay_to_client EXCEPTION: {type(e).__name__}: {e}")

                async def relay_to_target():
                    """Client → Streamlit."""
                    try:
                        while True:
                            raw = await websocket.receive()
                            if raw["type"] == "websocket.disconnect":
                                print(f"[ws] ← Client disconnected (code={raw.get('code', '?')})")
                                break
                            if raw["type"] == "websocket.receive":
                                if "bytes" in raw:
                                    print(f"[ws] ← client binary ({len(raw['bytes'])} bytes)")
                                    await ws.send_bytes(raw["bytes"])
                                elif "text" in raw:
                                    print(f"[ws] ← client text ({len(raw['text'])} chars)")
                                    await ws.send_str(raw["text"])
                    except Exception as e:
                        print(f"[ws] relay_to_target EXCEPTION: {type(e).__name__}: {e}")

                tasks = [asyncio.create_task(relay_to_client()), asyncio.create_task(relay_to_target())]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for t in pending:
                    t.cancel()
                print(f"[ws] Connection closed (done={len(done)}, cancelled={len(pending)})")
    except Exception as exc:
        print(f"[ws] Proxy EXCEPTION: {type(exc).__name__}: {exc}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.close(code=1011)
        except Exception:
            pass


# ===========================================================================
# Statyczne raporty AI
# ===========================================================================

AI_REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-reports")
if os.path.isdir(AI_REPORTS_DIR):
    app.mount("/ai-reports", StaticFiles(directory=AI_REPORTS_DIR), name="ai-reports")


# ===========================================================================
# Vue.js SPA — statyczne pliki + catch-all fallback
# ===========================================================================

VUE_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "vue")
if os.path.isdir(VUE_DIST):
    # Serwuj pliki statyczne Vue (assets, favicon itp.)
    app.mount("/assets", StaticFiles(directory=os.path.join(VUE_DIST, "assets")), name="vue-assets")

    from fastapi.responses import FileResponse

    @app.get("/{full_path:path}", include_in_schema=False)
    async def vue_spa(full_path: str):
        """SPA fallback — tylko ścieżki niezarezerwowane przez API/proxy."""
        # Nie ruszaj ścieżek Streamlit, API, WebSocket ani raportów AI
        if full_path.startswith(("streamlit/", "_stcore/", "api/", "ai-reports/")):
            return JSONResponse({"error": "Not found"}, status_code=404)

        file_path = os.path.join(VUE_DIST, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        index = os.path.join(VUE_DIST, "index.html")
        if os.path.isfile(index):
            return FileResponse(index, media_type="text/html")
        return JSONResponse({"error": "Vue app not built"}, status_code=404)
else:
    print(f"WARNING: Vue dist not found at {VUE_DIST}")


# ===========================================================================
# Dev server
# ===========================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run("App:app", host="0.0.0.0", port=port, reload=False)
