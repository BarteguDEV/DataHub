"""Aplikacja Flask z API REST i Vue.js SPA na froncie."""

import os
import random
from datetime import datetime, timedelta
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

APP_VERSION = "v0.2.0"

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
    db.create_all()
    try:
        admin = User(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Utworzono domyślnego użytkownika: admin / admin123")
    except IntegrityError:
        db.session.rollback()


# ---------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
