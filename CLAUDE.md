# DataHub — Project Memory

## Stack

| Warstwa | Technologia |
|---------|-------------|
| Backend | Python 3.12, FastAPI 0.139, Uvicorn |
| Frontend | Vue 3.4 (Composition API, `<script setup>`, JS, brak TS) |
| Build | Vite 5 |
| Streamlit | 1.59 — dashboard embedded w iframe |
| Baza | SQLite (dev), Oracle/Snowflake tylko w symulowanych raportach |
| Auth | JWT (python-jose + passlib, localStorage po stronie klienta) |
| Deploy | Azure App Service (Linux), startup: `uvicorn App:app` |

## Struktura katalogów

```
DataHub/
├── App.py                     # FastAPI — główny backend
├── streamlit_app.py           # Stub (przekierowuje do developers hub)
├── generate_ai_reports.py     # Generator 15 raportów HTML
├── generate_coverage.py       # Test coverage + commit
├── requirements.txt           # Python 73 pakiety
├── runtime.txt                # python-3.12.9
├── .env                       # JWT_SECRET, DATABASE_URL, STREAMLIT_PORT
├── startup.sh                 # Azure App Service
├── run_local.ps1              # Dev runner (PowerShell)
│
├── static/vue/                # Zbudowany Vue SPA (wynik npm run build)
├── ai-reports/                # 18 HTML raportów AI
├── vue-app/                   # Vue 3 SPA — główny frontend
│   ├── src/
│   │   ├── api.js             # Klient API z JWT
│   │   ├── router/index.js    # 6 route'ów
│   │   ├── stores/            # auth, version, width, theme
│   │   ├── components/        # AppHeader, ModuleCard
│   │   ├── views/             # LoginView, HubSelectView, etc.
│   │   └── hubs/
│   │       ├── planning/      # PlanningHubView (1700 linii)
│   │       ├── developers/    # DevelopersHubView + streamlit_app.py
│   │       ├── business/      # BusinessHubView (KPI, ETL, SLA)
│   │       └── ai/            # AiHubView (raporty AI)
│   └── package.json
├── vue-poc/                   # Prawdopodobnie porzucone
├── tests/                     # test_api.py, test_reports.py, test_streamlit_funcs.py
└── .github/workflows/         # tests.yml (CI/CD), deploy.yml (DEPRECATED)
```

## Routing Vue

| Ścieżka | Widok | Auth |
|---------|-------|------|
| `/login` | LoginView | gość |
| `/` | HubSelectView | wymagany |
| `/ddt` | DevelopersHubView | wymagany |
| `/business` | BusinessHubView | wymagany |
| `/ai` | AiHubView | wymagany |
| `/planning` | PlanningHubView | wymagany |

## Endpointy API (FastAPI)

- `GET /api/health` — health check + wersja
- `POST /api/login` — JWT login (username/password/system)
- `GET/POST/PUT/DELETE /api/planning/topics` — CRUD tematów (w pamięci!)
- `GET/POST/DELETE /api/planning/dependencies` — graf zależności (w pamięci!)
- `GET /api/business/*` — mockowane KPI, ETL, SLA
- `GET /streamlit/*` — reverse proxy do Streamlit

> **Uwaga**: Wszystkie dane Business i Planning są symulowane / w pamięci. Brak trwałego storage'u poza SQLite z użytkownikami.

## Huby — krótki opis

| Hub | Plik | Co robi |
|-----|------|---------|
| **Planning** | `hubs/planning/PlanningHubView.vue` | Tablica z tematami, ranking, matrix (2x2), graf zależności, roadmapa Gantt |
| **Developers** | `hubs/developers/DevelopersHubView.vue` | Embed Streamlit dashboardu migracji (Jira, Confluence, IAM, TeamCity, Informatica) |
| **Business** | `hubs/business/BusinessHubView.vue` | KPI, donut chart, ETL table, SLA, alerty — wszystko mock |
| **AI** | `hubs/ai/AiHubView.vue` | Galeria 15 raportów HTML (generowanych przez `generate_ai_reports.py`) |

## Streamlit

- Uruchamiany jako subprocess FastAPI (lifespan)
- Port: 8501 (`.env: STREAMLIT_PORT`)
- Dashboard: `vue-app/src/hubs/developers/streamlit_app.py` (535 linii)
- Proxy: HTTP (`aiohttp`) + WebSocket (`aiohttp`)
- Wszystkie dane symulowane (`numpy.random.default_rng`)

## Konwencje

### Wersjonowanie
Przed każdym commitem zmieniającym kod produkcyjny:

| Plik | Pole |
|------|------|
| `App.py` | `APP_VERSION = "v0.26.1"` → patch/minor/major |
| `vue-app/package.json` | `"version": "0.2.1"` → synchronicznie |
| `vue-app/src/hubs/developers/streamlit_app.py` | `st.caption("...v0.13.5")` → synchronicznie |

### Commity
- Conventional commits: `fix:`, `feat:`, `chore:`, `refactor:`, `docs:`
- Język: Polski w treści, angielski w typie (type(scope))
- Przykład: `fix(planning): dodaj brakujący closing tag w roadmap-view`

### Styl kodu (Vue)
- Composition API, `<script setup>`
- Brak TypeScript
- Brak biblioteki UI — własny CSS z custom properties
- Store'y: modułowe composable, nie Pinia
- v-if/v-else-if/v-else w chainach — pilnuj domknięć tagów

## Znane problemy / uwagi

- Planning Hub: dane giną przy restarcie serwera (storage w pamięci)
- Money Pits quadrant: tekst "Przeciągnij tematy tutaj" jest wewnątrz `v-for` zamiast w osobnym `v-if` empty state (bug)
- `vue-poc/` — wygląda na porzucony projekt, nie używać
- `deploy.yml` — DEPRECATED, nie używać
- `AppSidebar.vue` — istnieje ale nie jest renderowany
- JWT w localStorage — celowy trade-off dla prostoty
- Streamlit dashboard: cały modeling to symulacja, brak rzeczywistych API

## Polecenia uruchomieniowe

```bash
# Backend
uvicorn App:app --reload --port 5000

# Frontend (dev)
cd vue-app && npm run dev

# Frontend (build)
cd vue-app && npm run build

# Testy
pytest

# Streamlit osobno (debug)
streamlit run vue-app/src/hubs/developers/streamlit_app.py --server.port 8501
```

## Konfiguracja OpenCode

| Plik | Opis |
|------|------|
| `opencode.jsonc` | Konfiguracja projektu: permisje, referencje, instrukcje |
| `.learnings/LEARNINGS.md` | Log korekt, insightów i best practices |
| `.learnings/ERRORS.md` | Log błędów builda, tooli i API |
| `.learnings/FEATURE_REQUESTS.md` | Log pomysłów i żądań funkcji |

### Zasady self-improvement
- Gdy AI popełni błąd → log do `LEARNINGS.md` (kategoria `correction`)
- Gdy komenda / build padnie → log do `ERRORS.md`
- Gdy poprosisz o brakującą funkcję → log do `FEATURE_REQUESTS.md`
- Gdy coś powtarza się 3+ razy → promuj do tego pliku (`CLAUDE.md`)
```

## Pliki konfiguracyjne

- `.env` — JWT_SECRET, DATABASE_URL, STREAMLIT_PORT
- `pyproject.toml` — pytest + coverage config
- `.github/workflows/tests.yml` — CI/CD: testy + deploy do Azure
- `startup.sh` — Azure App Service entrypoint
