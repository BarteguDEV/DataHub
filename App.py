"""Aplikacja Flask z API REST i Vue.js SPA na froncie."""

import os
import random
import subprocess
import signal
import sys
import atexit
import time
import pathlib
from datetime import datetime, timedelta
from functools import wraps

import threading

import requests
import websocket as ws_client
from dotenv import load_dotenv
from flask import Flask, request, session, jsonify, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

APP_VERSION = "v0.3.0"

# ---------------------------------------------------------------------------
# App & DB
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())

DB_URL = os.getenv("DATABASE_URL") or "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Ścieżka do zbudowanej aplikacji Vue
VUE_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "vue")


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


# ---------------------------------------------------------------------------
# Helper — serwowanie Vue SPA
# ---------------------------------------------------------------------------

def serve_vue(path: str = ""):
    """Serwuje plik zbudowanej aplikacji Vue z SPA fallbackiem."""
    if path and os.path.exists(os.path.join(VUE_DIST, path)):
        return send_from_directory(VUE_DIST, path)
    index = os.path.join(VUE_DIST, "index.html")
    if os.path.exists(index):
        return send_from_directory(VUE_DIST, "index.html")
    return "Vue app not built. Run: cd vue-app && npm run build", 404


# ---------------------------------------------------------------------------
# API — JSON endpoints
# ---------------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Niepoprawna nazwa użytkownika lub hasło"}), 401

    session["user_id"] = user.id
    session["username"] = user.username
    session.permanent = True
    return jsonify({"ok": True, "user": {
        "id": user.id,
        "username": user.username,
        "role": "Developer",
        "initials": _compute_initials(user.username),
    }})


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Uzupełnij wszystkie pola"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Użytkownik już istnieje"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"ok": True}), 201


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify({"error": "Nie zalogowany"}), 401
    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "Użytkownik nie istnieje"}), 401
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": "Developer",
        "initials": _compute_initials(user.username),
    })


@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "ok",
        "service": "DataHub API",
        "version": APP_VERSION,
    })


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _compute_initials(username: str) -> str:
    parts = username.replace(".", " ").split()
    return "".join(p[0].upper() for p in parts if p)[:2]


# ---------------------------------------------------------------------------
# APEX — Business Intelligence (mock API)
# ---------------------------------------------------------------------------

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
    return [
        {"month": m, "transactions": random.randint(800, 3500), "errors": random.randint(5, 50)}
        for m in months
    ]


def _apex_reports():
    statuses = ["ready", "ready", "ready", "generating"]
    rows = []
    names = [
        "Raport_dzienny_KPI", "SLA_Compliance_Q2", "ETL_Performance_Weekly",
        "Data_Quality_Scorecard", "Capacity_Forecast_Q3", "Error_Analysis",
        "Cost_Tracker_MTD", "User_Activity_Report",
    ]
    authors = ["B. Gawron", "A. Kowalski", "K. Nowak", "System"]
    for i in range(8):
        rows.append({
            "id": i + 1,
            "name": random.choice(names) + "_" + datetime.now().strftime("%Y-%m-%d") + random.choice([".pdf", ".xlsx", ".html"]),
            "size": f"{random.randint(200, 5000)} KB",
            "date": (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
            "author": random.choice(authors),
            "status": random.choice(statuses),
        })
    return rows


def _apex_etl():
    workflows = ["LOAD_CUSTOMER", "LOAD_TRANSACTIONS", "SYNC_ACCOUNTS",
                 "CALC_INTEREST", "GEN_REPORT", "AGG_DAILY_KPI"]
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


@app.route("/api/apex/kpi")
def apex_kpi():
    return jsonify({"success": True, "data": _apex_kpi()})


@app.route("/api/apex/trends")
def apex_trends():
    return jsonify({"success": True, "data": _apex_trends()})


@app.route("/api/apex/reports")
def apex_reports():
    return jsonify({"success": True, "data": _apex_reports()})


@app.route("/api/apex/etl")
def apex_etl():
    return jsonify({"success": True, "data": _apex_etl()})


@app.route("/api/apex/sla")
def apex_sla():
    return jsonify({"success": True, "data": _apex_sla()})


@app.route("/api/apex/alerts")
def apex_alerts():
    return jsonify({"success": True, "data": _apex_alerts()})


# ---------------------------------------------------------------------------
# Statyczne raporty AI
# ---------------------------------------------------------------------------

AI_REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-reports")


@app.route("/ai-reports/<path:filename>")
def serve_ai_report(filename: str):
    """Serwuje wygenerowane raporty HTML z katalogu ai-reports/."""
    return send_from_directory(AI_REPORTS_DIR, filename)


# ---------------------------------------------------------------------------
# Streamlit — proxy HTTP + WebSocket do lokalnego serwera (port 8501)
# ---------------------------------------------------------------------------

STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
STREAMLIT_BASE = f"http://localhost:{STREAMLIT_PORT}"
STREAMLIT_WS_BASE = f"ws://localhost:{STREAMLIT_PORT}"

# ---------------------------------------------------------------------------
# Streamlit — subprocess manager
# ---------------------------------------------------------------------------

_streamlit_process = None
_STREAMLIT_PIDFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".streamlit.pid"
)


def _start_streamlit():
    """Uruchamia Streamlit jako subproces OS (jeśli jeszcze nie działa)."""
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
        "--browser.gatherUsageStats", "false",
    ]

    try:
        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True

        _streamlit_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **kwargs,
        )

        with open(_STREAMLIT_PIDFILE, "w") as f:
            f.write(str(_streamlit_process.pid))
        print(f"[streamlit] PID {_streamlit_process.pid} on port {STREAMLIT_PORT}")

        # Daj mu chwilę na start i sprawdź czy żyje
        time.sleep(2)
        if _streamlit_process.poll() is not None:
            print(f"[streamlit] WARNING — died immediately (code {_streamlit_process.returncode})")
        else:
            print(f"[streamlit] Started successfully")
    except Exception as e:
        print(f"[streamlit] ERROR — {e}")


def _is_streamlit_alive():
    """True jeśli Streamlit już działa (subprocess lub PID file)."""
    if _streamlit_process is not None and _streamlit_process.poll() is None:
        return True
    pidfile = pathlib.Path(_STREAMLIT_PIDFILE)
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            os.kill(pid, 0)          # signal 0 = sprawdź czy proces istnieje
            return True
        except (OSError, ValueError):
            pidfile.unlink(missing_ok=True)
    return False


def _stop_streamlit():
    """Zatrzymuje subproces Streamlit przy shutdownie."""
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


@app.route("/_stcore/<path:subpath>")
@app.route("/streamlit/_stcore/<path:subpath>")
def streamlit_ws_proxy(subpath: str):
    """Proxy WebSocket → Streamlit.
    Gevent-websocket wstrzykuje obiekt WebSocket do request.environ.
    """
    client_ws = request.environ.get("wsgi.websocket")
    if not client_ws:
        # Zwykłe HTTP — przekaż do HTTP proxy Streamlit
        return streamlit_http_proxy(f"_stcore/{subpath}")

    target_url = f"{STREAMLIT_WS_BASE}/_stcore/{subpath}"
    try:
        target = ws_client.create_connection(target_url, timeout=5)
    except Exception:
        return "Streamlit WebSocket unavailable", 502

    stop = threading.Event()

    def relay_to_client():
        """Streamlit → Client WebSocket."""
        try:
            while not stop.is_set():
                data = target.recv()
                if data is None:
                    break
                client_ws.send(data)
        except Exception:
            pass
        finally:
            stop.set()

    t = threading.Thread(target=relay_to_client, daemon=True)
    t.start()

    try:
        while not stop.is_set():
            data = client_ws.receive()
            if data is None:
                break
            target.send(data)
    except Exception:
        pass
    finally:
        stop.set()
        try:
            target.close()
        except Exception:
            pass

    return ""


# ---------------------------------------------------------------------------
# Streamlit — proxy HTTP
# ---------------------------------------------------------------------------


@app.route("/streamlit/", defaults={"path": ""})
@app.route("/streamlit/<path:path>")
def streamlit_http_proxy(path: str):
    """Proxy HTTP do serwera Streamlit uruchomionego na porcie 8501."""
    target = f"{STREAMLIT_BASE}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=target,
            headers={k: v for k, v in request.headers if k.lower() not in ("host",)},
            data=request.get_data(),
            cookies=request.cookies,
            stream=True,
            timeout=5,
        )
        excluded_headers = {
            "content-encoding", "transfer-encoding", "connection",
            "content-length", "server",
        }
        headers = [
            (k, v) for k, v in resp.headers.items()
            if k.lower() not in excluded_headers
        ]
        return Response(
            resp.iter_content(chunk_size=8192),
            status=resp.status_code,
            headers=headers,
        )
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Streamlit nie jest dostępny"}), 502


# ---------------------------------------------------------------------------
# Frontend — Vue.js SPA (catch-all; API routes above take priority)
# ---------------------------------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def vue_frontend(path: str = ""):
    return serve_vue(path)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found"}), 404


# ---------------------------------------------------------------------------
# Inicjalizacja bazy
# ---------------------------------------------------------------------------

with app.app_context():
    # Race condition między workerami gunicorna — SQLite nie lubi
    # równoczesnego CREATE TABLE. Wyłapujemy błąd i idziemy dalej.
    try:
        db.create_all()
    except OperationalError:
        pass

    try:
        admin = User(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Utworzono domyślnego użytkownika: admin / admin123")
    except IntegrityError:
        db.session.rollback()


# ---------------------------------------------------------------------------
# Start Streamlit (subprocess)
# ---------------------------------------------------------------------------

_start_streamlit()

# ---------------------------------------------------------------------------
# Start (dev)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
