# DataHub — Aplikacja Flask z logowaniem

Prosta aplikacja Flask z rejestracją i logowaniem użytkowników, gotowa do deployu na **Azure App Service**.

## Uruchomienie lokalne

```bash
# 1. Wirtualne środowisko
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # Linux/macOS

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom
python App.py
```

Aplikacja będzie dostępna pod adresem `http://localhost:5000`.

### Domyślny użytkownik

Przy pierwszym uruchomieniu automatycznie tworzone jest konto:

| Login | Hasło |
|-------|-------|
| admin | admin123 |

## Zmienne środowiskowe

| Zmienna | Opis | Domyślnie |
|---------|------|-----------|
| `SECRET_KEY` | Klucz do podpisywania sesji | (generowany losowo) |
| `DATABASE_URL` | URL bazy danych (SQLAlchemy) | `sqlite:///users.db` |
| `PORT` | Port serwera (używany przez Azure) | `5000` |

> **Na Azure** ustaw `SECRET_KEY` w **Application Settings** w portalu App Service.  
> Dla bazy produkcyjnej podmień `DATABASE_URL` na np. Azure SQL lub PostgreSQL.

## Deploy na Azure App Service

### Opcja A — przez Git (Azure CLI)

```bash
# Zaloguj do Azure
az login

# Utwórz App Service (Linux + Python)
az group create --nazwa moja-grupa --location westeurope
az webapp up --runtime "PYTHON:3.12" --sku B1 --location westeurope --nazwa datahub-app

# Ustaw zmienne środowiskowe
az webapp config appsettings set \
  --nazwa datahub-app \
  --resource-group moja-grupa \
  --settings SECRET_KEY="tutaj_wygenerowany_klucz"

# Ustaw komendę startową
az webapp config set \
  --nazwa datahub-app \
  --resource-group moja-grupa \
  --startup-file "gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=120 App:app"
```

### Opcja B — przez GitHub Actions (CI/CD)

W repozytorium GitHub:

1. Dodaj sekrety: `AZURE_WEBAPP_PUBLISH_PROFILE`, `SECRET_KEY`
2. Wrzuć plik `.github/workflows/deploy.yml` z workflowem deployu (opcjonalnie)

### Opcja C — przez Deployment Center w portalu

1. Wejdź w App Service → **Deployment Center**
2. Wybierz GitHub → swój repo → branch `main`
3. Portal sam skonfiguruje CI/CD

## Struktura projektu

```
DataHub/
├── App.py              # Główna aplikacja Flask
├── requirements.txt    # Zależności Pythona
├── startup.sh          # Skrypt startowy dla Azure (Linux)
├── .env                # Zmienne lokalne (nie commitować!)
├── .gitignore
├── README.md
└── templates/
    ├── base.html       # Szablon bazowy
    ├── login.html      # Strona logowania
    ├── register.html   # Strona rejestracji
    └── index.html      # Panel główny (po zalogowaniu)
```
