# DataHub — Portal integracyjny

FastAPI + Vue 3 + Streamlit.  
Centralne centrum monitoringu procesów biznesowych, migracji systemów i raportów AI.

## Wymagania

| Narzędzie | Minimalna wersja | Sprawdź |
|-----------|-----------------|---------|
| Python | 3.11+ | `python --version` |
| Node.js | 20+ | `node --version` |
| npm | 10+ | `npm --version` |

## Szybki start (Windows)

```powershell
# 1. Sklonuj repo
git clone <repo-url>
cd DataHub

# 2. Utwórz i aktywuj venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Zainstaluj zależności Python
pip install -r requirements.txt

# 4. Zainstaluj zależności frontendu
cd vue-app
npm install
cd ..

# 5. Zbuduj frontend
cd vue-app
npm run build
cd ..

# 6. Uruchom serwer
uvicorn App:app --host 0.0.0.0 --port 5000 --reload
```

Aplikacja dostępna pod `http://localhost:5000`.

---

## Szybki start (skrypt)

```powershell
.\run_local.ps1
```

Buduje Vue, generuje raporty AI i uruchamia serwer.

## Domyślni użytkownicy

| Login | Hasło | Rola |
|-------|-------|------|
| admin | admin123 | Developer |
| demo | demo123 | Developer |

## Zmienne środowiskowe (`.env`)

| Zmienna | Opis | Domyślnie |
|---------|------|-----------|
| `JWT_SECRET` | Klucz do JWT | (generowany losowo) |
| `DATABASE_URL` | URL bazy SQLAlchemy | `sqlite:///users.db` |
| `STREAMLIT_PORT` | Port Streamlit | `8501` |
| `PORT` | Port serwera FastAPI | `5000` |

## Wymagania

| Narzędzie | Wersja |
|-----------|--------|
| Python | 3.11+ |
| Node.js | 20+ |
| npm | 10+ |

## Uruchomienie krok po kroku

### 1. Backend (Python)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
source .venv/bin/activate            # Linux/macOS

pip install -r requirements.txt
pip install pytest pytest-cov       # do testów
```

### 2. Frontend (Vue)

```powershell
cd vue-app
npm install
npm run build
cd ..
```

### 3. Uruchom

```powershell
uvicorn App:app --host 0.0.0.0 --port 5000 --reload
```

Otwórz `http://localhost:5000`.

### 4. (opcjonalnie) Streamlit dashboard

Streamlit uruchamia się automatycznie jako subproces FastAPI.  
Dostępny pod `http://localhost:5000/streamlit/`.

## Testy

```bash
# Backend
pytest tests/ -v

# Z coverage
pytest tests/ --cov=. --cov-report=term

# Generuj raport coverage dla frontendu
python generate_coverage.py
```

## Struktura projektu

```
DataHub/
├── App.py                          # FastAPI backend
├── streamlit_app.py                # Streamlit dashboard (stub)
├── generate_coverage.py            # Generuje raport coverage
├── generate_ai_reports.py          # Generuje raporty AI
├── requirements.txt                # Zależności Python
├── .env                            # Zmienne lokalne
├── .gitignore
├── .github/workflows/
│   └── tests.yml                   # CI/CD Pipeline
├── static/
│   ├── test-coverage.json          # Raport coverage (generowany)
│   └── vue/                        # Zbudowany frontend (generowany)
├── vue-app/
│   ├── src/                        # Kod źródłowy Vue
│   │   ├── views/                  # Widoki (Login, HubSelect, itd.)
│   │   ├── hubs/                   # Huby (business, developers, ai)
│   │   ├── components/             # Komponenty (AppHeader, AppSidebar)
│   │   ├── stores/                 # Pinia stores (auth, version, width)
│   │   ├── router/                 # Vue Router
│   │   ├── api.js                  # Klient API z JWT
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── vue-app/src/hubs/developers/
│   └── streamlit_app.py           # Streamlit dashboard
├── tests/
│   ├── test_api.py                # Testy endpointów FastAPI
│   ├── test_streamlit_funcs.py    # Testy funkcji Streamlit
│   └── test_reports.py            # Testy raportów AI
├── generate_coverage.py           # Generator raportu coverage
├── generate_ai_reports.py         # Generator raportów AI
├── ai-reports/                    # Wygenerowane raporty AI
├── users.db                       # Baza SQLite (lokalnie)
└── .github/workflows/
    └── tests.yml                  # CI/CD Pipeline
```

## CI/CD

Po pushu na `main`/`master` GitHub Actions automatycznie:
1. Uruchamia testy backendu i frontendu
2. Generuje raport coverage
3. Buduje Vue SPA
4. Deployuje na Azure App Service

Wymagane **sekrety GitHub**:
- `AZURE_WEBAPP_NAME` — nazwa App Service
- `AZURE_WEBAPP_PUBLISH_PROFILE` — profil publikacji z Azure Portal
