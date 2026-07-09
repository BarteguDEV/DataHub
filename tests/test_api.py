"""
Testy endpointów FastAPI.
Uruchom:  pytest tests/ -v
Coverage: pytest tests/ --cov=. --cov-report=json
"""
from fastapi.testclient import TestClient
import sys
import os

# Dodaj katalog główny do ścieżki — pozwoli importować App.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from App import app

client = TestClient(app)


def test_health():
    """/api/health zwraca 200 z wersją."""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert "version" in data
    assert data["version"].startswith("v")


def test_login_missing_fields():
    """Login bez hasła → 422."""
    r = client.post("/api/login", json={"username": "admin"})
    assert r.status_code == 422


def test_login_wrong_password():
    """Login ze złym hasłem → 401."""
    r = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401
    assert "Niepoprawna" in r.json()["detail"]


def test_login_with_system():
    """Login z systemId → system w odpowiedzi."""
    r = client.post("/api/login", json={
        "username": "admin", "password": "admin123", "system": "EMIR_3"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["system"] == "EMIR_3"
    assert "access_token" in data


def test_me_unauthorized():
    """/api/me bez tokena → 401."""
    r = client.get("/api/me")
    assert r.status_code == 401


def test_me_authorized():
    """/api/me z tokenem → dane użytkownika."""
    login = client.post("/api/login", json={
        "username": "admin", "password": "admin123"
    }).json()
    token = login["access_token"]
    r = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "admin"


def test_business_kpi_unauthenticated():
    """KPI bez tokena → 401."""
    r = client.get("/api/business/kpi")
    assert r.status_code == 401


def test_business_kpi_authenticated():
    """KPI z tokenem → 200 + kluczowe pola w data."""
    login = client.post("/api/login", json={
        "username": "admin", "password": "admin123"
    }).json()
    token = login["access_token"]
    r = client.get("/api/business/kpi", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    kpi_data = data["data"]
    assert "uptime" in kpi_data
    assert "transactions" in kpi_data
    assert "sla" in kpi_data
    assert "avg_processing_sec" in kpi_data