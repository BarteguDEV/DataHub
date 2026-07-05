"""
APEX — Business Intelligence API (symulacja)
Dostarcza dane dashboardowe dla APEX Huba w Vue.js.
Endpointy zwracają JSON z mock danych.

Uruchom: python apex_api.py
Serwer: http://localhost:5100
"""

from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------
# SZTUCZNE DANE
# --------------------------------------------------------------

def random_kpi():
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


def monthly_trend():
    months = ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip"]
    return [
        {"month": m, "transactions": random.randint(800, 3500), "errors": random.randint(5, 50)}
        for m in months
    ]


def recent_reports():
    statuses = ["ready", "ready", "ready", "generating"]
    rows = []
    for i in range(8):
        rows.append({
            "id": i + 1,
            "name": random.choice([
                "Raport_dzienny_KPI", "SLA_Compliance_Q2", "ETL_Performance_Weekly",
                "Data_Quality_Scorecard", "Capacity_Forecast_Q3", "Error_Analysis",
                "Cost_Tracker_MTD", "User_Activity_Report",
            ]) + "_" + datetime.now().strftime("%Y-%m-%d") + random.choice([".pdf", ".xlsx", ".html"]),
            "size": f"{random.randint(200, 5000)} KB",
            "date": (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
            "author": random.choice(["B. Gawron", "A. Kowalski", "K. Nowak", "System"]),
            "status": random.choice(statuses),
        })
    return rows


def etl_performance():
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


def sla_data():
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


def system_alerts():
    levels = ["critical", "warning", "info"]
    sources = ["PowerCenter", "TeamCity", "Oracle", "Snowflake", "App Server"]
    return [
        {
            "id": i + 1,
            "level": random.choice(levels),
            "source": random.choice(sources),
            "message": random.choice([
                "Connection pool exhausted", "Table space > 85%",
                "Build failed: payment-gateway", "ETL workflow aborted",
                "Long running query detected", "Certificate expires in 7 days",
            ]),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
        }
        for i in range(6)
    ]

# --------------------------------------------------------------
# ENDPOINTY
# --------------------------------------------------------------

@app.route("/")
def index():
    return jsonify({
        "service": "APEX Business Intelligence API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "kpi": "/api/kpi",
            "trends": "/api/trends",
            "reports": "/api/reports",
            "etl": "/api/etl",
            "sla": "/api/sla",
            "alerts": "/api/alerts",
        },
    })


@app.route("/api/kpi")
def api_kpi():
    return jsonify({"success": True, "data": random_kpi()})


@app.route("/api/trends")
def api_trends():
    return jsonify({"success": True, "data": monthly_trend()})


@app.route("/api/reports")
def api_reports():
    return jsonify({"success": True, "data": recent_reports()})


@app.route("/api/etl")
def api_etl():
    return jsonify({"success": True, "data": etl_performance()})


@app.route("/api/sla")
def api_sla():
    return jsonify({"success": True, "data": sla_data()})


@app.route("/api/alerts")
def api_alerts():
    return jsonify({"success": True, "data": system_alerts()})


# --------------------------------------------------------------
# URUCHOMIENIE
# --------------------------------------------------------------
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════╗
║    APEX API — Business Intelligence      ║
║    http://localhost:5100                 ║
╚══════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=5100, debug=False)
