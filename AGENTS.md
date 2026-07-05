# 📋 POC Portal HUB Application

## 🔥 Najważniejsze informacje (MUST KNOW)

Uruchomienie aplikacji i kluczowym punktem startującym jest plik **`main.py`**. Po uruchomieniu działa backend APEX API (Flask) na porcie 5100 oraz frontend Vue.js z Vite na portie 3000. **Nie wymaga żadnych dodatkowych instrukcji ani instalacji** – po prostu uruchamiaj.

## 📦 Struktura repozytorium

- `backend/` → folder główny to backend aplikacji (np. API endpoints, modele danych)
- `frontend/` → folder głównej aplikacji frontendowej (np. Vue.js, React itp.)

## ⚙️ Konfigurowanie i środowisko

### Backend APEX API (Flask) na porcie 5100

Używane technologie: Flask, SQLite (domyślnie), sqlite3

Zasady dla backendu:
- Utrzymuj czystość danych i kodu. Wdroż zmiany bezpośrednio do plików.
- Upewnij się, że kod jest czytelny i zawiera odpowiednie komentarze wyjaśniające logikę biznesową (np. `# TODO: ...` zamiast `### TODO:`)

> ⚠️ Uwaga: Backend APEX API dostarcza **mock dane** (symulację), nie prawdziwe dane. Ten plik jest aktywny, więc pamiętaj o tym podczas pisania testów i implementacji nowych funkcjonalności!

#### Endpointy Flaska (z backend/apex_api.py):
- `/` → index()
- `/api/kpi` → api_kpi() (mock danych KPI)
- `/api/trends` → api_trends() (trend miesięczny)
- `/api/reports` → api_reports() (ostatnie raporty AI)
- `/api/etl` → api_etl() (performance workflows ETL)
- `/api/sla` → api_sla() (dane compliance SLA)
- `/api/alerts` → api_alerts() (system alerts)

### Frontend (Vue.js + Vite) na porcie 3000

Frontend jest uruchomiony automatycznie po starcie Flaska (backend). Port to **3000**.

#### Struktura plików frontendowych:
- Ściagawka plików w folderze `frontend/` zawiera tylko jeden dokument Markdown – `AGENTS.md`. To główny plik frontendowej aplikacji.

## 🚀 Jak uruchomić backend APEX API na porcie 5100?

Backend to Flask API, który dostarcza mock dane (symulację), nie prawdziwe dane!

Po prostu uruchom:
```bash
python main.py
Uruchomie zarówno backend (port 5100) jak i frontend (port 3000). Aplikacje działają automatycznie po starcie – przeglądarka powinna się otworzyć.
💡 Porady do pisania testów i implementacji w kodzie
- Upewnij się, że kod jest czytelny i zawiera odpowiednie komentarze wyjaśniające logikę biznesową.
- Jeśli coś wygląda niezrozumiale (np. ### TODO: ...) – upewnij się wcześniej, że to ma sens. Układaj to jak w prawdziwym życiu. 🎯
⚠️ Uwaga: Mock API
Backend APEX API dostarcza mock dane (symulację), nie prawdziwe dane. Jest to aktywny endpoint – pamiętaj o tym podczas pisania testów i implementacji nowych funkcjonalności!

Dobrze, teraz mogę spróbować jeszcze raz napisać plik AGENTS.md bezpośrednio w folderze docelowym:

```markdown
# 📋 POC Portal HUB Application

## 🔥 Najważniejsze informacje (MUST KNOW)

Uruchomienie aplikacji i kluczowym punktem startującym jest plik **`main.py`**. Po uruchomieniu działa backend APEX API (Flask) na porcie 5100 oraz frontend Vue.js z Vite na portie 3000. **Nie wymaga żadnych dodatkowych instrukcji ani instalacji** – po prostu uruchamiaj.

## 📦 Struktura repozytorium

- `backend/` → folder główny to backend aplikacji (np. API endpoints, modele danych)
- `frontend/` → folder głównej aplikacji frontendowej (np. Vue.js, React itp.)

## ⚙️ Konfigurowanie i środowisko

### Backend APEX API (Flask) na porcie 5100

Używane technologie: Flask, SQLite (domyślnie), sqlite3

Zasady dla backendu:
- Utrzymuj czystość danych i kodu. Wdroż zmiany bezpośrednio do plików.
- Upewnij się, że kod jest czytelny i zawiera odpowiednie komentarze wyjaśniające logikę biznesową (np. `# TODO: ...` zamiast `### TODO:`)

> ⚠️ Uwaga: Backend APEX API dostarcza **mock dane** (symulację), nie prawdziwe dane. Ten plik jest aktywny, więc pamiętaj o tym podczas pisania testów i implementacji nowych funkcjonalności!

#### Endpointy Flaska (z backend/apex_api.py):
- `/` → index()
- `/api/kpi` → api_kpi() (mock danych KPI)
- `/api/trends` → api_trends() (trend miesięczny)
- `/api/reports` → api_reports() (ostatnie raporty AI)
- `/api/etl` → api_etl() (performance workflows ETL)
- `/api/sla` → api_sla() (dane compliance SLA)
- `/api/alerts` → api_alerts() (system alerts)

### Frontend (Vue.js + Vite) na porcie 3000

Frontend jest uruchomiony automatycznie po starcie Flaska (backend). Port to **3000**.

#### Struktura plików frontendowych:
- Ściagawka plików w folderze `frontend/` zawiera tylko jeden dokument Markdown – `AGENTS.md`. To główny plik frontendowej aplikacji.

## 🚀 Jak uruchomić backend APEX API na porcie 5100?

Backend to Flask API, który dostarcza mock dane (symulację), nie prawdziwe dane!

Po prostu uruchom:
```bash
python main.py
Uruchomie zarówno backend (port 5100) jak i frontend (port 3000). Aplikacje działają automatycznie po starcie – przeglądarka powinna się otworzyć.
💡 Porady do pisania testów i implementacji w kodzie
- Upewnij się, że kod jest czytelny i zawiera odpowiednie komentarze wyjaśniające logikę biznesową.
- Jeśli coś wygląda niezrozumiale (np. ### TODO: ...) – upewnij się wcześniej, że to ma sens. Układaj to jak w prawdziwym życiu. 🎯
⚠️ Uwaga: Mock API
Backend APEX API dostarcza mock dane (symulację), nie prawdziwe dane. Jest to aktywny endpoint – pamiętaj o tym podczas pisania testów i implementacji nowych funkcjonalności!