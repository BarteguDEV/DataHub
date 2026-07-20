"""
DataHub — Streamlit Dashboard Narzędzi Deweloperskich.
Symulacja modułów: Jira, Confluence, IAM, TeamCity, Informatica.
"""
import time
import random
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from dataclasses import dataclass

st.set_page_config(
    page_title="DataHub — Dashboard Deweloperski",
    page_icon="⚙️",
    layout="wide",
)

# ===========================================================================
# Pomocnicze generatory danych
# ===========================================================================
RNG = np.random.default_rng(42)

@dataclass
class JiraTask:
    key: str
    summary: str
    issue_type: str  # Task, Change, SDJ, Xray
    status: str
    priority: str
    assignee: str
    created: str
    labels: str

@dataclass
class ConfluencePage:
    id: str
    title: str
    space: str
    version: int
    last_modified: str
    author: str
    content_html: str
    status: str  # current, archived, draft

@dataclass
class IAMGroup:
    name: str
    description: str
    members: int
    roles: list
    created: str

@dataclass
class IAMPermission:
    group: str
    resource: str
    action: str  # READ, WRITE, ADMIN, EXECUTE
    effect: str  # ALLOW, DENY

@dataclass
class TeamCityBuild:
    id: str
    pipeline: str
    branch: str
    status: str  # SUCCESS, FAILURE, RUNNING, QUEUED, CANCELLED
    triggered_by: str
    started: str
    duration_sec: int
    changes: int
    agent: str

# ===========================================================================
# Generatory HTML dla Confluence
# ===========================================================================
def _confluence_html_arch() -> str:
    return """<h1>Architektura Systemu DataHub v2</h1>
<p><em>Ostatnia modyfikacja: B.Gawron, 2 godziny temu</em></p>
<hr>
<h2>Diagram kontenerów</h2>
<div style="background:#f0f4f8;padding:16px;border-radius:8px;font-family:monospace;font-size:13px;line-height:1.5;">
<div style="border:2px solid #334155;border-radius:8px;padding:12px;margin-bottom:8px;background:#1e293b;color:#e2e8f0;text-align:center;font-weight:bold;">🌐 DataHub System</div>
<div style="display:flex;gap:8px;margin-bottom:8px;">
  <div style="flex:1;border:2px solid #3b82f6;border-radius:6px;padding:8px;text-align:center;background:#eff6ff;">
    <div style="font-weight:bold;color:#1e40af;">🖥️ Vue SPA</div>
    <div style="font-size:11px;color:#64748b;">:5173</div>
  </div>
  <div style="flex:1;border:2px solid #22c55e;border-radius:6px;padding:8px;text-align:center;background:#f0fdf4;">
    <div style="font-weight:bold;color:#166534;">📊 Streamlit</div>
    <div style="font-size:11px;color:#64748b;">:8501</div>
  </div>
  <div style="flex:1;border:2px solid #a855f7;border-radius:6px;padding:8px;text-align:center;background:#faf5ff;">
    <div style="font-weight:bold;color:#7e22ce;">⚡ FastAPI</div>
    <div style="font-size:11px;color:#64748b;">:5000</div>
  </div>
</div>
<div style="display:flex;justify-content:center;gap:4px;margin-bottom:8px;font-size:18px;color:#94a3b8;">
  <span>⬇️</span> <span>⬇️</span> <span>⬇️</span>
</div>
<div style="border:2px solid #f59e0b;border-radius:8px;padding:12px;text-align:center;background:#fffbeb;margin-bottom:8px;">
  <div style="font-weight:bold;color:#92400e;">☁️ Azure App Service (Linux)</div>
  <div style="font-size:12px;color:#d97706;">Nginx reverse-proxy → Streamlit / FastAPI</div>
</div>
<div style="display:flex;justify-content:center;gap:4px;margin-bottom:8px;font-size:18px;color:#94a3b8;">
  <span>⬇️</span>
</div>
<div style="display:flex;gap:8px;">
  <div style="flex:1;border:2px solid #94a3b8;border-radius:6px;padding:8px;text-align:center;background:#f8fafc;">
    <div style="font-weight:bold;color:#475569;">🗄️ SQLite</div>
    <div style="font-size:11px;color:#64748b;">(dev)</div>
  </div>
  <div style="flex:1;border:2px solid #ef4444;border-radius:6px;padding:8px;text-align:center;background:#fef2f2;">
    <div style="font-weight:bold;color:#991b1b;">🗄️ Oracle</div>
    <div style="font-size:11px;color:#64748b;">(prod)</div>
  </div>
  <div style="flex:1;border:2px solid #06b6d4;border-radius:6px;padding:8px;text-align:center;background:#ecfeff;">
    <div style="font-weight:bold;color:#155e75;">❄️ Snowflake</div>
    <div style="font-size:11px;color:#64748b;">(data lake)</div>
  </div>
</div>
</div>
<h2>Komponenty</h2>
<ul>
  <li><strong>FastAPI</strong> — backend REST, JWT auth, proxy do Streamlit</li>
  <li><strong>Vue 3 SPA</strong> — interfejs użytkownika (Composition API)</li>
  <li><strong>Streamlit</strong> — dashboard narzędzi deweloperskich (iframe)</li>
  <li><strong>SQLite</strong> — storage użytkowników (dev)</li>
  <li><strong>Oracle/Snowflake</strong> — tylko symulowane w raportach</li>
</ul>
<h2>Endpointy API</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Metoda</th><th>Ścieżka</th><th>Opis</th></tr>
<tr><td>GET</td><td>/api/health</td><td>Health check</td></tr>
<tr><td>POST</td><td>/api/login</td><td>Autentykacja JWT</td></tr>
<tr><td>GET</td><td>/api/planning/topics</td><td>Tematy planningu</td></tr>
<tr><td>GET</td><td>/api/business/kpi</td><td>KPI biznesowe</td></tr>
<tr><td>GET</td><td>/streamlit/</td><td>Proxy do Streamlit</td></tr>
</table>"""

def _confluence_html_deploy() -> str:
    return """<h1>Instrukcja Deployu na Azure</h1>
<p><em>Autor: A.Kowalski, wersja 1.8</em></p>
<hr>
<h2>Wymagania</h2>
<ul>
  <li>Azure CLI (az) — zalogowany na subskrypcję</li>
  <li>Python 3.12+</li>
  <li>Docker Desktop (opcjonalnie)</li>
</ul>
<h2>Kroki deployu</h2>
<pre style="background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;">
# 1. Build frontendu
cd vue-app && npm run build

# 2. Uruchom testy
pytest

# 3. Zbuduj i wypchnij obraz
az acr build --registry datahubacr --image datahub-app:latest .

# 4. Deploy do App Service
az webapp deploy --resource-group datahub-rg \
  --name datahub-app \
  --src-path deploy.zip

# 5. Restart
az webapp restart --name datahub-app --resource-group datahub-rg
</pre>
<h2>Konfiguracja startup.sh</h2>
<pre style="background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;">
#!/bin/bash
# Uruchom Streamlit w tle
streamlit run vue-app/src/hubs/developers/streamlit_app.py \
  --server.port 8501 --server.headless true &

# Uruchom FastAPI
uvicorn App:app --host 0.0.0.0 --port 5000
</pre>"""

def _confluence_html_security() -> str:
    return """<h1>Polityka Bezpieczeństwa IT</h1>
<p><em>Wersja 2.3, zatwierdzona przez CISO</em></p>
<hr>
<h2>Zasady ogólne</h2>
<ol>
  <li>Wszystkie hasła muszą mieć minimum 12 znaków</li>
  <li>MFA obowiązkowe dla wszystkich kont produkcyjnych</li>
  <li>Dostęp do bazy danych tylko przez VPN + bastion</li>
  <li>Logi przechowywane minimalnie 90 dni</li>
</ol>
<h2>Role bezpieczeństwa</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Rola</th><th>Zakres</th><th>Wymaga MFA</th></tr>
<tr><td>Administrator</td><td>Pełny dostęp</td><td>✅</td></tr>
<tr><td>Developer</td><td>Dev/Test</td><td>✅</td></tr>
<tr><td>Analityk</td><td>Tylko odczyt</td><td>✅</td></tr>
<tr><td>Gość</td><td>Publiczne API</td><td>❌</td></tr>
</table>
<h2>Audyt</h2>
<p>🔍 Ostatni audyt: <strong>2026-06-15</strong> — wynik: <span style="color:green;">✅ 96/100</span></p>
<p>📋 Zalecenia do poprawy: <strong>3</strong> (średnia ważność)</p>"""

def _confluence_html_api() -> str:
    return """<h1>API Reference — REST v2</h1>
<p><em>Ostatnia aktualizacja: B.Gawron</em></p>
<hr>
<h2>Autentykacja</h2>
<pre style="background:#1e1e2e;color:#cdd6f4;padding:12px;border-radius:6px;">
POST /api/login
{
  "username": "bgawron",
  "password": "***",
  "grant_type": "password"
}
→ 200 { "access_token": "eyJ...", "token_type": "bearer" }</pre>
<h2>Health Check</h2>
<pre style="background:#1e1e2e;color:#cdd6f4;padding:12px;border-radius:6px;">
GET /api/health
Authorization: Bearer &lt;token&gt;
→ 200 { "status": "ok", "version": "v0.32.0" }</pre>
<h2>Planning — Tematy</h2>
<pre style="background:#1e1e2e;color:#cdd6f4;padding:12px;border-radius:6px;">
POST /api/planning/topics
{
  "title": "Migracja Oracle→Snowflake",
  "category": "Technical Debt",
  "impact": 4,
  "effort": 3
}
→ 201 { "id": "...", "title": "..." }</pre>"""

def _confluence_html_runbook() -> str:
    return """<h1>Runbook — Alerty i Monitoring</h1>
<p><em>Autor: T.Wojcik, wersja 1.3</em></p>
<hr>
<h2>Alerty krytyczne</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Alert</th><th>Próg</th><th>Akcja</th></tr>
<tr><td>CPU > 90%</td><td>5 min</td><td>Restart instancji / skalowanie w górę</td></tr>
<tr><td>Błąd loginów > 5%</td><td>10 min</td><td>Sprawdź JWT / bazę użytkowników</td></tr>
<tr><td>Streamlit offline</td><td>Natychmiast</td><td>Restart subprocessu</td></tr>
<tr><td>Dysk > 85%</td><td>30 min</td><td>Czyszczenie logów / archiwizacja</td></tr>
</table>
<h2>Runbook krok po kroku</h2>
<h3>A: Streamlit nie odpowiada</h3>
<ol>
  <li>Sprawdź `ps aux | grep streamlit`</li>
  <li>Jeśli brak: `streamlit run ... &`</li>
  <li>Sprawdź logi: `tail -100 /var/log/streamlit.log`</li>
  <li>Jeśli port zajęty: `kill -9 $(lsof -t -i:8501)`</li>
</ol>
<h3>B: Wysokie zużycie pamięci</h3>
<ol>
  <li>Zaloguj się do Azure Portal</li>
  <li>App Service → skalowanie w poziomie (+1 instancja)</li>
  <li>Monitoruj przez 15 minut</li>
  <li>Jeśli bez zmian: zrestartuj App Service</li>
</ol>"""

def _confluence_html_python() -> str:
    return """<h1>Standardy Kodowania Python</h1>
<p><em>Autor: M.Zielinska, wersja 2.0</em></p>
<hr>
<h2>Wymagania</h2>
<ul>
  <li>Python 3.12+</li>
  <li>Black — formatowanie kodu (line-length=100)</li>
  <li>Ruff — linter</li>
  <li>MyPy — type checking (strict mode)</li>
</ul>
<h2>Struktura projektu</h2>
<pre style="background:#f0f4f8;padding:12px;border-radius:6px;">
src/
├── api/          # Endpointy FastAPI
├── core/         # Logika biznesowa
├── models/       # Pydantic / SQLAlchemy
├── services/     # Serwisy (JWT, proxy)
└── utils/        # Helpery
tests/
├── unit/
├── integration/
└── fixtures/</pre>
<h2>Konwencje nazewnicze</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Element</th><th>Styl</th><th>Przykład</th></tr>
<tr><td>Zmienne</td><td>snake_case</td><td>user_count</td></tr>
<tr><td>Funkcje</td><td>snake_case</td><td>get_user_by_id()</td></tr>
<tr><td>Klasy</td><td>PascalCase</td><td>UserRepository</td></tr>
<tr><td>Stałe</td><td>UPPER_CASE</td><td>MAX_RETRY_COUNT</td></tr>
</table>"""

def _confluence_html_migration() -> str:
    return """<h1>Harmonogram Migracji Q3 2026</h1>
<p><em>Aktualizacja: 2026-07-17</em></p>
<hr>
<h2>Kamienie milowe</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Moduł</th><th>Planowany termin</th><th>Status</th></tr>
<tr><td>Jira — wszystkie projekty</td><td>2026-08-15</td><td>🟡 72%</td></tr>
<tr><td>Confluence — space'y</td><td>2026-08-30</td><td>🟡 58%</td></tr>
<tr><td>IAM — użytkownicy</td><td>2026-07-30</td><td>🟢 91%</td></tr>
<tr><td>TeamCity — build configs</td><td>2026-09-15</td><td>🔴 45%</td></tr>
<tr><td>Informatica — workflowy</td><td>2026-09-30</td><td>🔴 33%</td></tr>
</table>
<h2>Zasoby</h2>
<ul>
  <li>Zespół A (B.Gawron, A.Kowalski) — Jira + Confluence</li>
  <li>Zespół B (K.Nowak, M.Zielinska) — IAM + TeamCity</li>
  <li>Zespół C (T.Wojcik) — Informatica</li>
</ul>"""

def _confluence_html_sla() -> str:
    return """<h1>SLA i KPI — Definicje</h1>
<p><em>Autor: K.Nowak, wersja 3.1</em></p>
<hr>
<h2>Service Level Agreements</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr><th>Usługa</th><th>SLA</th><th>Okno pomiaru</th></tr>
<tr><td>API DataHub</td><td>99.5%</td><td>Miesiąc</td></tr>
<tr><td>Streamlit Dashboard</td><td>99.0%</td><td>Tydzień</td></tr>
<tr><td>Raporty AI</td><td>98.5%</td><td>Miesiąc</td></tr>
<tr><td>Endpointy Planning</td><td>99.9%</td><td>Kwartał</td></tr>
</table>
<h2>Key Performance Indicators</h2>
<ul>
  <li><strong>API Response Time</strong> — p99 &lt; 500ms ✅</li>
  <li><strong>Auth Success Rate</strong> — > 99% ✅</li>
  <li><strong>Streamlit Uptime</strong> — 98.7% ⚠️ (target 99%)</li>
  <li><strong>Test Coverage</strong> — 87% 🟡 (target 90%)</li>
</ul>"""

def _confluence_html_draft() -> str:
    return """<h1>Draft: Nowa architektura danych</h1>
<div style="background:#fff3cd;padding:8px 16px;border-radius:6px;border-left:4px solid #ffc107;">
📝 <strong>Szkic — niezatwierdzony do wdrożenia</strong>
</div>
<hr>
<h2>Propozycja: Data Mesh</h2>
<p>Zastąpienie centralnego Data Lake modelem Data Mesh z domenami:</p>
<ul>
  <li>Domena Finansowa → Snowflake</li>
  <li>Domena CRM → Oracle</li>
  <li>Domena Operacyjna → Kafka + S3</li>
</ul>
<p>🔬 <strong>Kolejne kroki:</strong> Proof of Concept w Q4 2026</p>
<p>👥 <strong>Sponsor:</strong> Dyrektor IT</p>"""

def _confluence_html_report() -> str:
    return """<h1>Raport Tygodniowy Sprint #42</h1>
<p><em>Okres: 2026-07-14 do 2026-07-20</em></p>
<hr>
<h2>Podsumowanie</h2>
<ul>
  <li>✅ Zrealizowane: <strong>18</strong> zadań</li>
  <li>🔄 W toku: <strong>5</strong> zadań</li>
  <li>⏳ W backlogu: <strong>12</strong> zadań</li>
  <li>📈 Velocity: <strong>85</strong> story points</li>
</ul>
<h2>Najważniejsze osiągnięcia</h2>
<ol>
  <li>Wdrożenie nowego endpointu raportów KPI</li>
  <li>Migracja bazy testowej do PostgreSQL</li>
  <li>Aktualizacja biblioteki pandas do wersji 2.2</li>
  <li>Setup CI/CD dla gałęzi release/*</li>
</ol>
<h2>Blokery</h2>
<p>🔴 <strong>CR-0433</strong> — oczekuje na approval architekta (3 dni)</p>"""

def _init_jira_backlog() -> list:
    issue_types = ["Task", "Change", "SDJ", "Xray"]
    statuses = ["To Do", "In Progress", "Review", "Done", "Blocked"]
    priorities = ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"]
    assignees = ["B.Gawron", "A.Kowalski", "K.Nowak", "M.Zielinska", "T.Wojcik", "Nieprzypisany"]
    labels_pool = ["frontend", "backend", "migration", "security", "performance", "uat", "prod"]
    summaries = {
        "Task": [
            "Implementacja endpointu raportów KPI",
            "Refaktoryzacja modułu autoryzacji",
            "Dodanie walidacji JSON Schema",
            "Aktualizacja biblioteki pandas do 2.2",
            "Optymalizacja zapytań do Snowflake",
            "Migracja bazy Oracle → PostgreSQL",
            "Czyszczenie logów z poprzedniego sprintu",
            "Setup środowiska dev na Kubernetes",
        ],
        "Change": [
            "CR-0421: Zmiana formatu daty w raporcie miesięcznym",
            "CR-0425: Dodanie kolumny 'region' do widoku sprzedaży",
            "CR-0430: Modyfikacja progu alertu SLA z 95% na 98%",
            "CR-0433: Zmiana endpointu API z v1 na v2",
            "CR-0438: Nowe reguły maskowania PII w logach",
        ],
        "SDJ": [
            "SDJ-112: Audyt bezpieczeństwa - zalecenie 4.2",
            "SDJ-115: Testy penetracyjne API Gateway",
            "SDJ-118: Review polityki haseł - wymóg SOX",
            "SDJ-121: Implementacja DLP na strumieniach danych",
        ],
        "Xray": [
            "XRAY-201: Testy regresji modułu CRM",
            "XRAY-205: Automatyzacja testów ETL pipeline",
            "XRAY-208: Testy wydajnościowe - 10k req/s",
            "XRAY-212: Walidacja raportów合规性",
        ],
    }
    backlog = []
    for i in range(40):
        itype = RNG.choice(issue_types)
        summary = RNG.choice(summaries[itype])
        key_num = RNG.integers(1000, 9999)
        backlog.append(JiraTask(
            key=f"{itype.upper()[:1] if itype != 'SDJ' else 'SDJ'}-{key_num}",
            summary=f"{summary} #T{key_num}",
            issue_type=itype,
            status=RNG.choice(statuses, p=[0.30, 0.20, 0.15, 0.25, 0.10]),
            priority=RNG.choice(priorities, p=[0.10, 0.25, 0.40, 0.25]),
            assignee=RNG.choice(assignees, p=[0.20, 0.20, 0.15, 0.15, 0.10, 0.20]),
            created=(datetime.now() - timedelta(days=int(RNG.integers(1, 90)))).strftime("%Y-%m-%d"),
            labels=", ".join(RNG.choice(labels_pool, int(RNG.integers(1, 4)))),
        ))
    return backlog

def _init_confluence_pages() -> list:
    pages = [
        ConfluencePage("P-100", "Architektura Systemu DataHub v2", "DOK-ARCH", 12,
                       (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), "B.Gawron",
                        _confluence_html_arch(), "current"),
        ConfluencePage("P-101", "Instrukcja Deployu na Azure", "DOK-OPS", 8,
                       (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "A.Kowalski",
                       _confluence_html_deploy(), "current"),
        ConfluencePage("P-102", "Polityka Bezpieczeństwa IT", "DOK-SEC", 5,
                       (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"), "K.Nowak",
                       _confluence_html_security(), "current"),
        ConfluencePage("P-103", "API Reference — REST v2", "DOK-DEV", 15,
                       (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"), "B.Gawron",
                       _confluence_html_api(), "current"),
        ConfluencePage("P-104", "Runbook — Alerty i Monitoring", "DOK-OPS", 6,
                       (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M"), "T.Wojcik",
                       _confluence_html_runbook(), "current"),
        ConfluencePage("P-105", "Standardy Kodowania Python", "DOK-DEV", 20,
                       (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M"), "M.Zielinska",
                       _confluence_html_python(), "current"),
        ConfluencePage("P-106", "Harmonogram Migracji Q3 2026", "DOK-ERP", 3,
                       (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"), "A.Kowalski",
                       _confluence_html_migration(), "current"),
        ConfluencePage("P-107", "SLA i KPI — Definicje", "DOK-FIN", 7,
                       (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"), "K.Nowak",
                       _confluence_html_sla(), "current"),
        ConfluencePage("P-108", "Draft: Nowa architektura danych", "DOK-ARCH", 2,
                       (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "B.Gawron",
                       _confluence_html_draft(), "draft"),
        ConfluencePage("P-109", "Raport Tygodniowy Sprint #42", "DOK-HR", 1,
                       (datetime.now() - timedelta(hours=12)).strftime("%Y-%m-%d %H:%M"), "M.Zielinska",
                       _confluence_html_report(), "current"),
    ]
    return pages

def _init_iam_groups() -> list:
    return [
        IAMGroup("datahub-admins", "Administratorzy DataHub", 5, ["ADMIN", "WRITE", "READ"], "2025-11-15"),
        IAMGroup("datahub-devs", "Zespół developerski", 12, ["WRITE", "READ"], "2025-11-20"),
        IAMGroup("datahub-analysts", "Analitycy danych", 8, ["READ", "EXECUTE"], "2025-12-01"),
        IAMGroup("datahub-readonly", "Dostęp tylko do odczytu", 24, ["READ"], "2026-01-10"),
        IAMGroup("etl-operators", "Operatorzy ETL", 6, ["EXECUTE", "READ"], "2026-02-05"),
        IAMGroup("security-auditors", "Audytorzy bezpieczeństwa", 3, ["READ", "ADMIN"], "2026-02-15"),
        IAMGroup("crm-integration", "Integracja CRM", 4, ["WRITE", "READ", "EXECUTE"], "2026-03-01"),
        IAMGroup("bi-reporting", "Raporty BI", 7, ["READ", "EXECUTE"], "2026-03-10"),
    ]

def _init_iam_permissions() -> list:
    resources = ["datapipe:prod:write", "datapipe:dev:write", "api:admin", "api:read",
                  "snowflake:warehouse", "s3:data-lake", "kafka:produce", "kafka:consume",
                  "oracle:finrep", "vault:secrets"]
    groups = [g.name for g in _init_iam_groups()]
    perms = []
    for g in _init_iam_groups():
        for r in RNG.choice(resources, int(RNG.integers(2, 5))):
            perms.append(IAMPermission(
                group=g.name,
                resource=r,
                action=RNG.choice(["READ", "WRITE", "ADMIN", "EXECUTE"]),
                effect="ALLOW",
            ))
    return perms

def _init_teamcity_builds() -> list:
    pipelines = ["data-ingestion", "etl-core", "reporting-service", "crm-sync",
                  "data-quality", "ml-pipeline", "api-gateway", "dwh-load"]
    agents = ["tc-agent-linux-01", "tc-agent-linux-02", "tc-agent-win-01",
              "tc-agent-docker-01", "tc-agent-docker-02"]
    devs = ["B.Gawron", "A.Kowalski", "K.Nowak", "M.Zielinska", "T.Wojcik", "GitHub Merge"]
    builds = []
    for i in range(50):
        pipeline = RNG.choice(pipelines)
        status = RNG.choice(["SUCCESS", "FAILURE", "RUNNING", "QUEUED", "CANCELLED"],
                           p=[0.55, 0.12, 0.08, 0.20, 0.05])
        duration = int(RNG.integers(30, 1800)) if status == "SUCCESS" else (
            int(RNG.integers(10, 600)) if status == "FAILURE" else 0
        )
        builds.append(TeamCityBuild(
            id=f"TC-{1000+i}",
            pipeline=pipeline,
            branch=RNG.choice(["main", "develop", "feature/*", "release/*", "hotfix/*"]),
            status=status,
            triggered_by=RNG.choice(devs),
            started=(datetime.now() - timedelta(minutes=int(RNG.integers(5, 1440)))).strftime("%Y-%m-%d %H:%M"),
            duration_sec=duration,
            changes=int(RNG.integers(1, 30)),
            agent=RNG.choice(agents),
        ))
    return sorted(builds, key=lambda b: b.started, reverse=True)

def _init_teamcity_pipelines() -> list:
    pipelines = ["data-ingestion", "etl-core", "reporting-service", "crm-sync",
                 "data-quality", "ml-pipeline", "api-gateway", "dwh-load"]
    data = []
    for p in pipelines:
        last_status = RNG.choice(["SUCCESS", "SUCCESS", "SUCCESS", "FAILURE", "RUNNING"])
        data.append({
            "Pipeline": p,
            "Last Status": last_status,
            "Success Rate": f"{RNG.integers(85, 100)}%",
            "Avg Time": f"{int(RNG.integers(2, 25))}m {int(RNG.integers(0, 59))}s",
            "Total Builds": int(RNG.integers(50, 500)),
            "Branches": int(RNG.integers(3, 12)),
            "Agent Pool": RNG.choice(["Linux", "Windows", "Docker", "Kubernetes"]),
        })
    return data

# ===========================================================================
# Inicjalizacja stanu sesji (must be after all _init_* functions)
# ===========================================================================
if "tab_idx" not in st.session_state:
    st.session_state.tab_idx = 0

if "page_views" not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

if "usage_counters" not in st.session_state:
    st.session_state.usage_counters = {
        "jira_tasks_created": 0,
        "jira_views": 0,
        "confluence_views": 0,
        "confluence_pages_rendered": 0,
        "iam_api_calls": 0,
        "iam_groups_created": 0,
        "teamcity_builds_triggered": 0,
        "teamcity_views": 0,
        "informatica_deployments": 0,
        "informatica_steps_run": 0,
    }

if "jira_backlog" not in st.session_state:
    st.session_state.jira_backlog = _init_jira_backlog()

if "confluence_pages" not in st.session_state:
    st.session_state.confluence_pages = _init_confluence_pages()

if "iam_groups" not in st.session_state:
    st.session_state.iam_groups = _init_iam_groups()

if "iam_permissions" not in st.session_state:
    st.session_state.iam_permissions = _init_iam_permissions()

if "teamcity_builds" not in st.session_state:
    st.session_state.teamcity_builds = _init_teamcity_builds()

if "teamcity_pipelines" not in st.session_state:
    st.session_state.teamcity_pipelines = _init_teamcity_pipelines()

if "informatica_log" not in st.session_state:
    st.session_state.informatica_log = []

# ===========================================================================
# Helper functions
# ===========================================================================
def _status_emoji(status: str) -> str:
    emojis = {
        "SUCCESS": "✅", "FAILURE": "❌", "RUNNING": "🔄", "QUEUED": "⏳",
        "CANCELLED": "🚫", "To Do": "📋", "In Progress": "🔄", "Review": "👀",
        "Done": "✅", "Blocked": "🚫", "current": "🟢", "draft": "📝", "archived": "📦",
    }
    return emojis.get(status, "❓")

def _priority_color(priority: str) -> str:
    if "Critical" in priority: return "🔴"
    if "High" in priority: return "🟠"
    if "Medium" in priority: return "🟡"
    return "🟢"

uc = st.session_state.usage_counters
total_actions = sum(uc.values())

# ===========================================================================
# Główny nagłówek
# ===========================================================================
st.title("⚙️ Dashboard Narzędzi Deweloperskich")
st.caption("Symulacja narzędzi: Jira · Confluence · IAM · TeamCity · Informatica")

# ===========================================================================
# Zakładki
# ===========================================================================
TAB_NAMES = [
    "📊 Statystyki", "🔷 Jira", "📄 Confluence",
    "🔐 IAM", "🔧 TeamCity", "⚡ Informatica",
]

cols = st.columns(len(TAB_NAMES))
for i, (col, name) in enumerate(zip(cols, TAB_NAMES)):
    with col:
        if st.button(
            name,
            use_container_width=True,
            type="primary" if st.session_state.tab_idx == i else "secondary",
        ):
            st.session_state.tab_idx = i
            st.rerun()

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# ===========================================================================
# TAB 0 — STATYSTYKI (dawniej Przegląd)
# ===========================================================================
if st.session_state.tab_idx == 0:
    st.subheader("📊 Statystyki aplikacji")

    # --- KPI overall ---
    kpi_cols = st.columns(5)
    with kpi_cols[0]:
        st.metric("🔷 Taski Jira", f"{len(st.session_state.jira_backlog)}", "40 w backlogu")
    with kpi_cols[1]:
        active_pages = sum(1 for p in st.session_state.confluence_pages if p.status == "current")
        st.metric("📄 Strony Confluence", f"{active_pages}", f"{len(st.session_state.confluence_pages)} łącznie")
    with kpi_cols[2]:
        st.metric("🔐 Grupy IAM", f"{len(st.session_state.iam_groups)}",
                  f"{len(st.session_state.iam_permissions)} uprawnień")
    with kpi_cols[3]:
        failed = sum(1 for b in st.session_state.teamcity_builds if b.status == "FAILURE")
        total = len(st.session_state.teamcity_builds)
        st.metric("🔧 Buildy TeamCity", f"{total}",
                  f"{failed} failed ({failed/max(1,total)*100:.0f}%)")
    with kpi_cols[4]:
        st.metric("⚡ Deploye Informatica", f"{uc['informatica_deployments']}",
                  f"{uc['informatica_steps_run']} kroków")

    st.markdown("#### 📈 Liczniki użycia (sesja)")
    counter_df = pd.DataFrame([
        {"Moduł": "Jira", "Akcja": "Utworzone taski", "Ilość": uc["jira_tasks_created"]},
        {"Moduł": "Jira", "Akcja": "Wyświetlenia", "Ilość": uc["jira_views"]},
        {"Moduł": "Confluence", "Akcja": "Wyświetlenia", "Ilość": uc["confluence_views"]},
        {"Moduł": "Confluence", "Akcja": "Renderowane strony", "Ilość": uc["confluence_pages_rendered"]},
        {"Moduł": "IAM", "Akcja": "Wywołania API", "Ilość": uc["iam_api_calls"]},
        {"Moduł": "IAM", "Akcja": "Utworzone grupy", "Ilość": uc["iam_groups_created"]},
        {"Moduł": "TeamCity", "Akcja": "Wyzwolone buildy", "Ilość": uc["teamcity_builds_triggered"]},
        {"Moduł": "TeamCity", "Akcja": "Wyświetlenia", "Ilość": uc["teamcity_views"]},
        {"Moduł": "Informatica", "Akcja": "Deploymenty", "Ilość": uc["informatica_deployments"]},
        {"Moduł": "Informatica", "Akcja": "Kroki wykonane", "Ilość": uc["informatica_steps_run"]},
    ])
    st.dataframe(counter_df, use_container_width=True, hide_index=True)

    st.markdown("#### 🏷️ Typy zadań Jira")
    jira_types = pd.DataFrame({
        "Typ": ["Task", "Change", "SDJ", "Xray"],
        "Ilość": [
            sum(1 for t in st.session_state.jira_backlog if t.issue_type == "Task"),
            sum(1 for t in st.session_state.jira_backlog if t.issue_type == "Change"),
            sum(1 for t in st.session_state.jira_backlog if t.issue_type == "SDJ"),
            sum(1 for t in st.session_state.jira_backlog if t.issue_type == "Xray"),
        ],
    })
    st.dataframe(jira_types, use_container_width=True, hide_index=True)

    st.markdown("#### 🔧 Statusy pipeline'ów TeamCity")
    pipeline_status = pd.DataFrame({
        "Status": ["SUCCESS", "FAILURE", "RUNNING", "QUEUED", "CANCELLED"],
        "Ilość": [
            sum(1 for b in st.session_state.teamcity_builds if b.status == "SUCCESS"),
            sum(1 for b in st.session_state.teamcity_builds if b.status == "FAILURE"),
            sum(1 for b in st.session_state.teamcity_builds if b.status == "RUNNING"),
            sum(1 for b in st.session_state.teamcity_builds if b.status == "QUEUED"),
            sum(1 for b in st.session_state.teamcity_builds if b.status == "CANCELLED"),
        ],
    })
    st.dataframe(pipeline_status, use_container_width=True, hide_index=True)

    # --- Reset liczników ---
    if st.button("🔄 Resetuj liczniki użycia"):
        for k in st.session_state.usage_counters:
            st.session_state.usage_counters[k] = 0
        st.rerun()

# ===========================================================================
# TAB 1 — JIRA
# ===========================================================================
elif st.session_state.tab_idx == 1:
    st.subheader("🔷 Jira — Backlog i Zarządzanie Zadaniami")
    st.session_state.usage_counters["jira_views"] += 1

    if "jira_flash" in st.session_state:
        st.success(st.session_state.jira_flash)
        del st.session_state.jira_flash

    backlog = st.session_state.jira_backlog

    # --- Dashboard ---
    d_cols = st.columns(4)
    with d_cols[0]:
        st.metric("📋 Łącznie zadań", len(backlog))
    with d_cols[1]:
        todo = sum(1 for t in backlog if t.status == "To Do")
        in_progress = sum(1 for t in backlog if t.status == "In Progress")
        st.metric("🔄 W toku", in_progress, f"{todo} w backlogu")
    with d_cols[2]:
        done = sum(1 for t in backlog if t.status == "Done")
        st.metric("✅ Zrobione", done)
    with d_cols[3]:
        blocked = sum(1 for t in backlog if t.status == "Blocked")
        st.metric("🚫 Zablokowane", blocked)

    # --- Typy zadań ---
    st.markdown("#### 🏷️ Typy zadań")
    type_cols = st.columns(4)
    for col, itype in zip(type_cols, ["Task", "Change", "SDJ", "Xray"]):
        count = sum(1 for t in backlog if t.issue_type == itype)
        with col:
            st.metric(itype, count)

    # --- Filtrowanie ---
    st.markdown("#### 🔍 Filtrowanie backlogu")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_type = st.selectbox("Typ zadania", ["Wszystkie", "Task", "Change", "SDJ", "Xray"])
    with f_col2:
        filter_status = st.selectbox("Status", ["Wszystkie", "To Do", "In Progress", "Review", "Done", "Blocked"])
    with f_col3:
        filter_assignee = st.selectbox("Przypisane do", ["Wszyscy"] + sorted(set(t.assignee for t in backlog)))

    filtered = backlog
    if filter_type != "Wszystkie":
        filtered = [t for t in filtered if t.issue_type == filter_type]
    if filter_status != "Wszystkie":
        filtered = [t for t in filtered if t.status == filter_status]
    if filter_assignee != "Wszyscy":
        filtered = [t for t in filtered if t.assignee == filter_assignee]

    # --- Tabela backlogu ---
    df_backlog = pd.DataFrame([
        {
            "Key": t.key,
            "Typ": t.issue_type,
            "Summary": t.summary[:60] + "..." if len(t.summary) > 60 else t.summary,
            "Status": f"{_status_emoji(t.status)} {t.status}",
            "Priorytet": f"{_priority_color(t.priority)} {t.priority}",
            "Assignee": t.assignee,
            "Utworzono": t.created,
            "Etykiety": t.labels,
        }
        for t in filtered
    ])
    st.dataframe(df_backlog, use_container_width=True, hide_index=True)

    # --- Tworzenie nowego zadania ---
    st.markdown("#### ➕ Utwórz nowe zadanie")
    with st.expander("Nowe zadanie Jira", expanded=False):
        with st.form("new_jira_task"):
            n_col1, n_col2 = st.columns(2)
            with n_col1:
                new_type = st.selectbox("Typ zadania", ["Task", "Change", "SDJ", "Xray"])
                new_summary = st.text_input("Tytuł", "Wpisz tytuł zadania...")
                new_priority = st.selectbox("Priorytet", ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"])
            with n_col2:
                new_assignee = st.selectbox("Przypisz do", ["B.Gawron", "A.Kowalski", "K.Nowak", "M.Zielinska", "T.Wojcik"])
                new_labels = st.text_input("Etykiety (po przecinku)", "backend, migration")
                new_desc = st.text_area("Opis", value="Opis zadania...")
            submitted = st.form_submit_button("📥 Utwórz zadanie", type="primary", use_container_width=True)
            if submitted and new_summary:
                prefix = new_type.upper()[:1] if new_type != "SDJ" else "SDJ"
                key_num = RNG.integers(1000, 9999)
                new_task = JiraTask(
                    key=f"{prefix}-{key_num}",
                    summary=new_summary,
                    issue_type=new_type,
                    status="To Do",
                    priority=new_priority,
                    assignee=new_assignee,
                    created=datetime.now().strftime("%Y-%m-%d"),
                    labels=new_labels,
                )
                st.session_state.jira_backlog.append(new_task)
                st.session_state.usage_counters["jira_tasks_created"] += 1
                st.session_state.jira_flash = (
                    f"✅ Utworzono {new_task.key} | {new_type} | "
                    f"'{new_summary}' → {new_assignee}"
                )
                st.rerun()

    # --- Statystyki projektów ---
    st.markdown("#### 📊 Podsumowanie według typu")
    type_summary = pd.DataFrame([
        {
            "Typ": it,
            "Ilość": sum(1 for t in backlog if t.issue_type == it),
            "To Do": sum(1 for t in backlog if t.issue_type == it and t.status == "To Do"),
            "In Progress": sum(1 for t in backlog if t.issue_type == it and t.status == "In Progress"),
            "Review": sum(1 for t in backlog if t.issue_type == it and t.status == "Review"),
            "Done": sum(1 for t in backlog if t.issue_type == it and t.status == "Done"),
            "Blocked": sum(1 for t in backlog if t.issue_type == it and t.status == "Blocked"),
        }
        for it in ["Task", "Change", "SDJ", "Xray"]
    ])
    st.dataframe(type_summary, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 2 — CONFLUENCE
# ===========================================================================
elif st.session_state.tab_idx == 2:
    st.subheader("📄 Confluence — Przeglądarka Stron")
    st.session_state.usage_counters["confluence_views"] += 1

    pages = st.session_state.confluence_pages

    # --- Dashboard ---
    c_cols = st.columns(4)
    with c_cols[0]:
        st.metric("📄 Strony", len(pages))
    with c_cols[1]:
        st.metric("🟢 Aktywne", sum(1 for p in pages if p.status == "current"))
    with c_cols[2]:
        st.metric("📝 Szkice", sum(1 for p in pages if p.status == "draft"))
    with c_cols[3]:
        st.metric("🏷️ Space'y", len(set(p.space for p in pages)))

    # --- Stan wybranej strony ---
    if "confluence_selected_id" not in st.session_state:
        st.session_state.confluence_selected_id = None

    # --- Lista stron ---
    st.markdown("#### 📋 Lista stron")
    page_data = pd.DataFrame([
        {
            "ID": p.id,
            "Tytuł": p.title,
            "Space": p.space,
            "Wersja": p.version,
            "Autor": p.author,
            "Ostatnia modyfikacja": p.last_modified,
            "Status": _status_emoji(p.status),
        }
        for p in pages
    ])
    st.dataframe(page_data, use_container_width=True, hide_index=True)

    # --- Renderowanie wybranej strony ---
    st.markdown("#### 👁️ Podgląd strony")

    render_col1, render_col2 = st.columns([1, 3])
    with render_col1:
        st.markdown("**Szybki podgląd**")
        for p in pages:
            label = p.title[:30] + "..." if len(p.title) > 30 else p.title
            if st.button(f"{_status_emoji(p.status)} {label}", use_container_width=True,
                         key=f"render_{p.id}"):
                st.session_state.confluence_selected_id = p.id
                st.session_state.usage_counters["confluence_pages_rendered"] += 1
                st.rerun()

    with render_col2:
        selected_id = st.session_state.confluence_selected_id
        selected_page = next((p for p in pages if p.id == selected_id), None)

        if selected_page:
            status_label = {
                "current": "🟢 Aktualna",
                "draft": "📝 Szkic",
                "archived": "📦 Zarchiwizowana",
            }.get(selected_page.status, selected_page.status)

            st.markdown(
                f"**{selected_page.title}** · {status_label} · "
                f"v{selected_page.version} · {selected_page.author} · {selected_page.last_modified}"
            )

            html_content = selected_page.content_html
            st.markdown(
                f'<div style="background:white;color:#1a1a2e;padding:24px;'
                f'border-radius:8px;border:1px solid #e2e8f0;'
                f'font-family:sans-serif;line-height:1.6;">'
                f'{html_content}</div>',
                unsafe_allow_html=True,
            )

            a_col1, a_col2, a_col3 = st.columns(3)
            with a_col1:
                if st.button("✏️ Edytuj stronę", use_container_width=True, key=f"edit_{selected_page.id}"):
                    st.info(f"📝 Edytor otwarty dla **{selected_page.title}** — symulacja edycji")
            with a_col2:
                if st.button("📋 Kopiuj link", use_container_width=True, key=f"copy_{selected_page.id}"):
                    page_url = f"https://confluence.company.com/display/{selected_page.space}/{selected_page.id}"
                    st.success(f"🔗 Link skopiowany: `{page_url}`")
            with a_col3:
                if st.button("📥 Eksport PDF", use_container_width=True, key=f"pdf_{selected_page.id}"):
                    st.info(f"📄 Generowanie PDF dla **{selected_page.title}**...")
                    time.sleep(0.5)
                    st.success("✅ PDF wygenerowany i gotowy do pobrania (symulacja)")
        else:
            st.info("👈 Wybierz stronę klikając przycisk szybkiego podglądu")

    # --- Statystyki space'ów ---
    st.markdown("#### 🏷️ Statystyki space'ów")
    space_stats = pd.DataFrame([
        {
            "Space": s,
            "Stron": sum(1 for p in pages if p.space == s),
            "Aktywne": sum(1 for p in pages if p.space == s and p.status == "current"),
            "Szkice": sum(1 for p in pages if p.space == s and p.status == "draft"),
        }
        for s in sorted(set(p.space for p in pages))
    ])
    st.dataframe(space_stats, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 3 — IAM
# ===========================================================================
elif st.session_state.tab_idx == 3:
    st.subheader("🔐 IAM — Zarządzanie Tożsamością (REST API)")
    st.session_state.usage_counters["iam_api_calls"] += 1

    iam_groups = st.session_state.iam_groups
    iam_perms = st.session_state.iam_permissions

    # --- Dashboard ---
    i_cols = st.columns(4)
    with i_cols[0]:
        st.metric("👥 Grupy", len(iam_groups))
    with i_cols[1]:
        st.metric("🔑 Uprawnienia", len(iam_perms))
    with i_cols[2]:
        st.metric("👤 Użytkowników (sym.)", sum(g.members for g in iam_groups))
    with i_cols[3]:
        st.metric("📋 Ról unikalnych", len(set(p.action for p in iam_perms)))

    # --- REST API Simulator ---
    st.markdown("#### 🌐 REST API — Symulator")
    st.caption("Symulacja wywołań REST API do systemu IAM")

    rest_col1, rest_col2 = st.columns([1, 2])
    with rest_col1:
        api_method = st.selectbox("Metoda HTTP", ["GET", "POST", "PUT", "DELETE"])
        api_endpoint = st.selectbox("Endpoint", [
            "/api/iam/groups",
            "/api/iam/groups/{name}",
            "/api/iam/permissions",
            "/api/iam/permissions/{id}",
            "/api/iam/roles",
            "/api/iam/users",
        ])
        api_body_area = st.empty()

    with rest_col2:
        st.markdown("**🔹 Parametry zapytania**")
        if "groups" in api_endpoint and "{" not in api_endpoint:
            if api_method == "POST":
                new_group_name = st.text_input("Nazwa grupy", "new-team-group")
                new_group_desc = st.text_input("Opis", "Nowa grupa dla zespołu")
                new_group_members = st.number_input("Liczba członków", 1, 100, 5)

                if st.button("📤 Wyślij POST /api/iam/groups", type="primary", use_container_width=True):
                    log_lines = []
                    log_lines.append(f">> POST /api/iam/groups")
                    log_lines.append(f">> Body: {{'name': '{new_group_name}', 'description': '{new_group_desc}'}}")
                    log_lines.append(f">> Headers: Authorization: Bearer **** | Content-Type: application/json")
                    log_lines.append(f"")
                    time.sleep(0.3)
                    log_lines.append(f"<< 201 Created")
                    log_lines.append(f"<< Location: /api/iam/groups/{new_group_name}")
                    log_lines.append(f"<< Response: {{'id': '{new_group_name}', 'status': 'active'}}")
                    log_lines.append(f"<< ✅ Grupa '{new_group_name}' utworzona pomyślnie")

                    # Dodaj do listy
                    st.session_state.iam_groups.append(IAMGroup(
                        name=new_group_name,
                        description=new_group_desc,
                        members=new_group_members,
                        roles=["READ"],
                        created=datetime.now().strftime("%Y-%m-%d"),
                    ))
                    st.session_state.usage_counters["iam_groups_created"] += 1
                    st.session_state.usage_counters["iam_api_calls"] += 1

                    st.code("\n".join(log_lines), language="text")
                    st.success(f"✅ Grupa '{new_group_name}' utworzona!")

            elif api_method == "GET":
                if st.button("📤 Wyślij GET /api/iam/groups", type="primary", use_container_width=True):
                    log_lines = [f">> GET /api/iam/groups"]
                    log_lines.append(">> Headers: Authorization: Bearer ****")
                    log_lines.append("")
                    time.sleep(0.2)
                    log_lines.append(f"<< 200 OK")
                    log_lines.append(f"<< [{', '.join(g.name for g in iam_groups)}]")
                    log_lines.append(f"<< Liczba grup: {len(iam_groups)}")
                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")

        elif "permissions" in api_endpoint and "{" not in api_endpoint:
            if api_method == "POST":
                perm_group = st.selectbox("Grupa", [g.name for g in iam_groups], key="perm_group")
                perm_resource = st.text_input("Zasób", "datapipe:prod:write")
                perm_action = st.selectbox("Akcja", ["READ", "WRITE", "ADMIN", "EXECUTE"])
                perm_effect = st.selectbox("Efekt", ["ALLOW", "DENY"])

                if st.button("📤 Wyślij POST /api/iam/permissions", type="primary", use_container_width=True):
                    log_lines = [f">> POST /api/iam/permissions"]
                    log_lines.append(f">> Body: {{'group': '{perm_group}', 'resource': '{perm_resource}', 'action': '{perm_action}', 'effect': '{perm_effect}'}}")
                    log_lines.append("")
                    time.sleep(0.3)
                    log_lines.append(f"<< 201 Created")
                    log_lines.append(f"<< Permission added: {perm_group} → {perm_action} on {perm_resource}")
                    log_lines.append(f"<< ✅ Uprawnienie nadane pomyślnie")

                    st.session_state.iam_permissions.append(IAMPermission(
                        group=perm_group,
                        resource=perm_resource,
                        action=perm_action,
                        effect=perm_effect,
                    ))
                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")
                    st.success(f"✅ Uprawnienie {perm_action} dla {perm_group} na {perm_resource}")

            elif api_method == "GET":
                if st.button("📤 Wyślij GET /api/iam/permissions", type="primary", use_container_width=True):
                    log_lines = [f">> GET /api/iam/permissions"]
                    log_lines.append(">> Headers: Authorization: Bearer ****")
                    log_lines.append("")
                    time.sleep(0.2)
                    log_lines.append(f"<< 200 OK")
                    log_lines.append(f"<< Liczba uprawnień: {len(iam_perms)}")
                    for p in iam_perms[:8]:
                        log_lines.append(f"   {p.group} | {p.action} | {p.resource} | {p.effect}")
                    if len(iam_perms) > 8:
                        log_lines.append(f"   ... i {len(iam_perms) - 8} więcej")
                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")

        elif "{name}" in api_endpoint:
            group_names = [g.name for g in iam_groups]
            selected_group = st.selectbox("Wybierz grupę", group_names)

            if api_method == "GET":
                if st.button("📤 Wyślij GET", type="primary", use_container_width=True):
                    g = next((g for g in iam_groups if g.name == selected_group), None)
                    log_lines = [f">> GET /api/iam/groups/{selected_group}"]
                    log_lines.append("")
                    time.sleep(0.2)
                    if g:
                        log_lines.append(f"<< 200 OK")
                        log_lines.append(f"<< {{'name': '{g.name}', 'description': '{g.description}', 'members': {g.members}, 'roles': {g.roles}, 'created': '{g.created}'}}")
                    else:
                        log_lines.append(f"<< 404 Not Found")
                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")

            elif api_method == "PUT":
                new_desc = st.text_input("Nowy opis", "Zaktualizowany opis grupy")
                if st.button("📤 Wyślij PUT", type="primary", use_container_width=True):
                    log_lines = [f">> PUT /api/iam/groups/{selected_group}"]
                    log_lines.append(f">> Body: {{'description': '{new_desc}'}}")
                    log_lines.append("")
                    time.sleep(0.3)
                    log_lines.append(f"<< 200 OK")
                    log_lines.append(f"<< Grupa '{selected_group}' zaktualizowana")
                    log_lines.append(f"<< description: '{new_desc}'")

                    # Update in place
                    for g in iam_groups:
                        if g.name == selected_group:
                            g.description = new_desc
                            break

                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")
                    st.success(f"✅ Grupa '{selected_group}' zaktualizowana")

            elif api_method == "DELETE":
                if st.button(f"🗑️ Usuń grupę {selected_group}", type="secondary", use_container_width=True):
                    log_lines = [f">> DELETE /api/iam/groups/{selected_group}"]
                    log_lines.append("")
                    time.sleep(0.3)
                    log_lines.append(f"<< 204 No Content")
                    log_lines.append(f"<< ✅ Grupa '{selected_group}' usunięta")

                    st.session_state.iam_groups = [g for g in iam_groups if g.name != selected_group]
                    st.session_state.usage_counters["iam_api_calls"] += 1
                    st.code("\n".join(log_lines), language="text")
                    st.success(f"✅ Grupa '{selected_group}' usunięta!")

        elif api_endpoint == "/api/iam/roles":
            if st.button("📤 Wyślij GET /api/iam/roles", type="primary", use_container_width=True):
                all_actions = set(p.action for p in iam_perms)
                log_lines = [f">> GET /api/iam/roles"]
                log_lines.append("")
                time.sleep(0.2)
                log_lines.append(f"<< 200 OK")
                for a in sorted(all_actions):
                    count = sum(1 for p in iam_perms if p.action == a)
                    log_lines.append(f"   {a}: {count} przypisań")
                st.session_state.usage_counters["iam_api_calls"] += 1
                st.code("\n".join(log_lines), language="text")

        elif api_endpoint == "/api/iam/users":
            if st.button("📤 Wyślij GET /api/iam/users", type="primary", use_container_width=True):
                total_users = sum(g.members for g in iam_groups)
                log_lines = [f">> GET /api/iam/users"]
                log_lines.append("")
                time.sleep(0.2)
                log_lines.append(f"<< 200 OK")
                log_lines.append(f"<< Łączna liczba użytkowników: {total_users}")
                for g in iam_groups:
                    log_lines.append(f"   {g.name}: {g.members} członków")
                st.session_state.usage_counters["iam_api_calls"] += 1
                st.code("\n".join(log_lines), language="text")

    # --- Lista grup ---
    st.markdown("#### 👥 Lista grup IAM")
    groups_df = pd.DataFrame([
        {"Nazwa": g.name, "Opis": g.description, "Członkowie": g.members,
         "Role": ", ".join(g.roles), "Utworzono": g.created}
        for g in iam_groups
    ])
    st.dataframe(groups_df, use_container_width=True, hide_index=True)

    # --- Lista uprawnień ---
    st.markdown("#### 🔑 Uprawnienia")
    perms_df = pd.DataFrame([
        {"Grupa": p.group, "Zasób": p.resource, "Akcja": p.action, "Efekt": p.effect}
        for p in iam_perms
    ])
    st.dataframe(perms_df, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 4 — TEAMCITY
# ===========================================================================
elif st.session_state.tab_idx == 4:
    st.subheader("🔧 TeamCity — CI/CD Pipeline'y i Buildy")
    st.session_state.usage_counters["teamcity_views"] += 1

    builds = st.session_state.teamcity_builds
    pipelines = st.session_state.teamcity_pipelines

    # --- Dashboard ---
    t_cols = st.columns(5)
    with t_cols[0]:
        st.metric("📦 Pipeline'y", len(pipelines))
    with t_cols[1]:
        st.metric("🏗️ Wszystkie buildy", len(builds))
    with t_cols[2]:
        failed = sum(1 for b in builds if b.status == "FAILURE")
        st.metric("❌ Wywalone", failed, f"{failed/max(1,len(builds))*100:.1f}%")
    with t_cols[3]:
        running = sum(1 for b in builds if b.status == "RUNNING")
        st.metric("🔄 W trakcie", running)
    with t_cols[4]:
        queued = sum(1 for b in builds if b.status == "QUEUED")
        st.metric("⏳ W kolejce", queued)

    # --- Pipeline overview ---
    st.markdown("#### 📊 Status pipeline'ów")
    pipes_df = pd.DataFrame(pipelines)
    pipes_df["Last Status"] = pipes_df["Last Status"].apply(
        lambda x: f"{_status_emoji(x)} {x}"
    )
    st.dataframe(pipes_df, use_container_width=True, hide_index=True)

    # --- Build history ---
    st.markdown("#### 📋 Historia buildów")
    build_df = pd.DataFrame([
        {
            "ID": b.id,
            "Pipeline": b.pipeline,
            "Branch": b.branch,
            "Status": f"{_status_emoji(b.status)} {b.status}",
            "Triggered By": b.triggered_by,
            "Started": b.started,
            "Duration": f"{b.duration_sec//60}m {b.duration_sec%60}s" if b.duration_sec > 0 else "-",
            "Changes": b.changes,
            "Agent": b.agent,
        }
        for b in builds[:30]
    ])
    st.dataframe(build_df, use_container_width=True, hide_index=True)

    # --- Failed builds highlight ---
    st.markdown("#### ❌ Ostatnie wywalone buildy")
    failed_builds = [b for b in builds if b.status == "FAILURE"]
    if failed_builds:
        fail_df = pd.DataFrame([
            {
                "ID": b.id,
                "Pipeline": b.pipeline,
                "Branch": b.branch,
                "Triggered By": b.triggered_by,
                "Started": b.started,
                "Duration": f"{b.duration_sec//60}m {b.duration_sec%60}s",
                "Changes": b.changes,
            }
            for b in failed_builds[:10]
        ])
        st.dataframe(fail_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ Brak wywalonych buildów")

    # --- Flash message ---
    if "tc_flash" in st.session_state:
        st.success(st.session_state.tc_flash)
        del st.session_state.tc_flash

    # --- Trigger build ---
    st.markdown("#### ▶️ Wyzwól build")
    with st.expander("Nowy build", expanded=False):
        trig_col1, trig_col2 = st.columns(2)
        with trig_col1:
            pipeline_choice = st.selectbox("Pipeline", [p["Pipeline"] for p in pipelines])
            branch_choice = st.selectbox("Branch", ["main", "develop", "feature/nowa-funkcja", "hotfix/critical-fix"])
        with trig_col2:
            trigger_user = st.selectbox("Wyzwalacz", ["B.Gawron", "A.Kowalski", "K.Nowak", "M.Zielinska", "T.Wojcik"])
            agent_pool = st.selectbox("Agent pool", ["Linux", "Windows", "Docker", "Kubernetes"])

        if st.button("🚀 Wyzwól build", type="primary", use_container_width=True):
            log_lines = []
            log_lines.append(f">> Trigger build on {pipeline_choice} ({branch_choice})")
            log_lines.append(f">> Triggered by: {trigger_user}")
            log_lines.append(f">> Agent pool: {agent_pool}")
            time.sleep(0.5)
            log_lines.append("")
            log_lines.append("<< Queued build TC-NEW-" + str(RNG.integers(100, 999)))
            log_lines.append("<< Agent assigned: " + RNG.choice(
                ["tc-agent-linux-01", "tc-agent-linux-02", "tc-agent-docker-01"])
            )
            log_lines.append("<< ✅ Build started successfully")
            log_lines.append("")

            # Add simulated build
            new_build = TeamCityBuild(
                id=f"TC-NEW-{RNG.integers(100, 999)}",
                pipeline=pipeline_choice,
                branch=branch_choice,
                status="QUEUED",
                triggered_by=trigger_user,
                started=datetime.now().strftime("%Y-%m-%d %H:%M"),
                duration_sec=0,
                changes=int(RNG.integers(1, 15)),
                agent="pending",
            )
            st.session_state.teamcity_builds.insert(0, new_build)
            st.session_state.usage_counters["teamcity_builds_triggered"] += 1
            st.code("\n".join(log_lines), language="text")
            st.session_state.tc_flash = f"✅ Build wyzwolony na {pipeline_choice}/{branch_choice}"
            st.rerun()

    # --- Agents ---
    st.markdown("#### 🖥️ Agenci")
    agents = ["tc-agent-linux-01", "tc-agent-linux-02", "tc-agent-win-01",
              "tc-agent-docker-01", "tc-agent-docker-02"]
    agent_pools = ["Linux", "Linux", "Windows", "Docker", "Kubernetes"]
    agent_statuses = ["✅ Online", "✅ Online", "⚠️ Busy", "✅ Online", "🔴 Offline"]
    agent_uptime = ["12d 4h", "7d 2h", "2d 15h", "1d 8h", "0d 0h"]
    agent_builds = [142, 89, 203, 56, 0]

    agents_df = pd.DataFrame({
        "Agent": agents,
        "Pool": agent_pools,
        "Status": agent_statuses,
        "Uptime": agent_uptime,
        "Completed Builds": agent_builds,
    })
    st.dataframe(agents_df, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 5 — INFORMATICA
# ===========================================================================
elif st.session_state.tab_idx == 5:
    st.subheader("⚡ Informatica — Deployment Grupy ETL")

    # --- Dashboard ---
    inf_cols = st.columns(4)
    with inf_cols[0]:
        st.metric("📦 Deploymenty", uc["informatica_deployments"])
    with inf_cols[1]:
        st.metric("👣 Kroki", uc["informatica_steps_run"])
    with inf_cols[2]:
        st.metric("⏱️ Ostatni", "—" if not st.session_state.informatica_log else "OK")
    with inf_cols[3]:
        st.metric("🔄 W kolejce", random.randint(0, 3))

    # --- Formularz deploymentu ---
    st.markdown("#### 🚀 Automatyczne tworzenie deployment grupy")
    st.caption("Wypełnij dane i uruchom symulację procesu deploymentu")

    with st.form("informatica_deploy_form"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            repo_url = st.text_input(
                "URL repozytorium",
                "https://git.company.com/zz_cicd/informatica-deploy.git",
                help="Repozytorium z kodem ETL",
            )
            tech_user = st.text_input(
                "Użytkownik techniczny",
                "zz_cicd",
                help="Service account do deploymentu",
            )
            folder_name = st.text_input(
                "Nazwa folderu",
                "30__finrep__emir_3",
                help="Nazwa folderu w repozytorium (zz_cicd/[folder])",
            )
        with f_col2:
            export_comment = st.text_area(
                "Komentarz do eksportu",
                value="Deployment EMIR_3 — wersja 2.1.0\nZmiany: dodanie nowego workflowu LOAD_EMIR_COUNTERPARTIES",
                height=100,
            )
            target_env = st.selectbox(
                "Środowisko docelowe",
                ["DEV", "TEST", "PROD"],
            )
            include_schemas = st.multiselect(
                "Opcje dodatkowe",
                ["Include dependencies", "Overwrite existing", "Skip validation", "Notify on finish"],
                default=["Include dependencies"],
            )

        submitted = st.form_submit_button("⚡ Uruchom deployment", type="primary", use_container_width=True)

    # --- Symulacja deploymentu ---
    if submitted:
        st.session_state.usage_counters["informatica_deployments"] += 1
        log_area = st.empty()
        progress_bar = st.progress(0, text="Inicjalizacja deploymentu...")
        status_placeholder = st.empty()

        steps = [
            ("export_workflow", "📦 Eksport workflow z repozytorium", 0.10),
            ("create_label", "🏷️ Tworzenie labelu w repozytorium", 0.25),
            ("create_query", "🔍 Tworzenie query w Informatica Catalog", 0.40),
            ("create_deployment_group", "📁 Tworzenie deployment group", 0.60),
            ("change_owner_label", "👤 Zmiana właściciela — label", 0.75),
            ("change_owner_query", "👤 Zmiana właściciela — query", 0.85),
            ("change_owner_deployment_group", "👤 Zmiana właściciela — deployment group", 0.95),
            ("finish", "✅ Deployment zakończony", 1.00),
        ]

        logs = []
        log_entry = st.empty()

        for step_id, step_name, progress_val in steps:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ▶️ {step_name}...")
            log_area.code("\n".join(logs), language="text")
            progress_bar.progress(progress_val, text=f"{step_name} ({int(progress_val*100)}%)")

            # Symulacja czasu wykonania
            time.sleep(0.4 + RNG.random() * 0.6)

            # Specyficzne logi dla każdego kroku
            if step_id == "export_workflow":
                logs.append(f"   ├─ Repo: {repo_url}")
                logs.append(f"   ├─ Folder: {folder_name}")
                logs.append(f"   ├─ Znaleziono {RNG.integers(5, 20)} workflowów")
                logs.append(f"   └─ ✅ Eksport zakończony ({RNG.uniform(1.2, 4.5):.1f}s)")
            elif step_id == "create_label":
                label_name = f"deploy_{folder_name.lower().replace('__', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                logs.append(f"   ├─ Tworzenie labelu: {label_name}")
                logs.append(f"   ├─ Commit: {RNG.choice(['a1b2c3d', 'e4f5g6h', 'x7y8z9a'])}{RNG.bytes(4).hex()}")
                logs.append(f"   └─ ✅ Label utworzony")
                st.session_state.informatica_log.append(f"Label: {label_name}")
            elif step_id == "create_query":
                query_name = f"QRY_DEPLOY_{folder_name.upper()[:12]}"
                logs.append(f"   ├─ Tworzenie query: {query_name}")
                logs.append(f"   ├─ Scope: {folder_name}/*.xml")
                logs.append(f"   ├─ Mapping: {RNG.choice(['EMIR_LOAD', 'COUNTERPARTIES_SYNC', 'REPORT_GEN'])}")
                logs.append(f"   └─ ✅ Query utworzone (ID: Q-{RNG.integers(1000, 9999)})")
                st.session_state.informatica_log.append(f"Query: {query_name}")
            elif step_id == "create_deployment_group":
                dg_name = f"DG_{folder_name.upper()[:10]}_{target_env}"
                logs.append(f"   ├─ Tworzenie deployment group: {dg_name}")
                logs.append(f"   ├─ Środowisko: {target_env}")
                logs.append(f"   ├─ Liczba obiektów: {RNG.integers(8, 30)}")
                logs.append(f"   └─ ✅ Deployment group utworzona (ID: DG-{RNG.integers(100, 999)})")
                st.session_state.informatica_log.append(f"DeploymentGroup: {dg_name}")
            elif step_id == "change_owner_label":
                new_owner = tech_user
                logs.append(f"   ├─ Zmiana właściciela label → {new_owner}")
                logs.append(f"   ├─ Stary właściciel: {RNG.choice(['informatica_admin', 'etl_service', 'deploy_bot'])}")
                logs.append(f"   └─ ✅ Właściciel labelu zmieniony na {new_owner}")
            elif step_id == "change_owner_query":
                logs.append(f"   ├─ Zmiana właściciela query → {tech_user}")
                logs.append(f"   ├─ Uprawnienia: OWNER, MODIFY, READ")
                logs.append(f"   └─ ✅ Właściciel query zmieniony na {tech_user}")
            elif step_id == "change_owner_deployment_group":
                logs.append(f"   ├─ Zmiana właściciela deployment group → {tech_user}")
                logs.append(f"   ├─ Dodatkowe granty: DEPLOY, VIEW")
                logs.append(f"   └─ ✅ Właściciel deployment group zmieniony na {tech_user}")
            elif step_id == "finish":
                logs.append(f"   ├─ Komentarz: {export_comment[:50]}...")
                logs.append(f"   ├─ Całkowity czas: {RNG.uniform(3.5, 12.0):.1f}s")
                logs.append(f"   └─ ✅ Deployment grupy zakończony sukcesem!")

            logs.append("")
            log_area.code("\n".join(logs), language="text")
            st.session_state.usage_counters["informatica_steps_run"] += 1

        progress_bar.progress(1.0, text="✅ Deployment zakończony!")
        status_placeholder.success("✅ Proces deploymentu zakończony pomyślnie!")

    # --- Historia deploymentów ---
    st.markdown("#### 📋 Historia deploymentów")
    if st.session_state.informatica_log:
        hist_df = pd.DataFrame({
            "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M") for _ in st.session_state.informatica_log],
            "Zdarzenie": st.session_state.informatica_log,
        })
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.info("Brak historii deploymentów. Uruchom pierwszy deployment.")

    # --- Deployment summary table ---
    st.markdown("#### 📊 Podsumowanie workflowów ETL")
    etl_workflows = ["LOAD_CUSTOMER", "LOAD_TRANSACTIONS", "SYNC_ACCOUNTS",
                     "LOAD_EMIR_COUNTERPARTIES", "CALC_INTEREST", "GEN_REPORT",
                     "AGG_KPI", "DATA_QUALITY", "ARCHIVE_LOGS"]
    etl_statuses = ["✅ Deployed", "✅ Deployed", "🔄 In Progress",
                    "✅ Deployed", "⏳ Pending", "❌ Error",
                    "✅ Deployed", "🔄 In Progress", "⏳ Pending"]
    try:
        current_folder = folder_name  # from form if submitted
    except NameError:
        current_folder = "30__finrep__emir_3"
    etl_df = pd.DataFrame({
        "Workflow": etl_workflows,
        "Folder": [current_folder for _ in etl_workflows],
        "Źródło": RNG.choice(["Oracle", "Snowflake", "SQL Server", "API", "File"], 9),
        "Cel": RNG.choice(["Snowflake", "Oracle", "DataLake", "Kafka"], 9),
        "Rekordy": [f"{RNG.integers(10, 5000)}k" for _ in range(9)],
        "Status": etl_statuses,
    })
    st.dataframe(etl_df, use_container_width=True, hide_index=True)

# ===========================================================================
# Footer
# ===========================================================================
st.markdown("---")
st.caption(f"DataHub — Streamlit Dashboard Deweloperski | v0.21.0 | "
           f"Liczba akcji w sesji: {total_actions}")
