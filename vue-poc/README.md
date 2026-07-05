# Vue POC — DataHub

Minimalny projekt Vue 3 + Vite potwierdzający, że Vue.js działa na Azure.

## Uruchomienie lokalne

```bash
cd vue-poc
npm install
npm run dev
```

→ `http://localhost:3000`

## Deploy na Azure Static Web Apps (darmowy)

### 1. Azure Portal — utwórz Static Web App

```
Azure Portal → Static Web Apps → Utwórz
  - Subskrypcja: twoja
  - Grupa zasobów: nowa lub istniejąca
  - Nazwa: datahub-vue-poc
  - Region: West Europe
  - Plan: Free (F1) ← darmowy
  - Źródło: GitHub
  - Organizacja: BarteguDEV
  - Repozytorium: DataHub
  - Gałąź: main
  - Lokalizacja kodu: vue-poc
  - Framework: Vue.js
```

Azure sam wygeneruje GitHub Actions workflow i doda go do repozytorium.

### 2. Alternatywnie — dodaj workflow ręcznie

Utwórz plik `.github/workflows/azure-static-web-apps.yml` (Azure wygeneruje go automatycznie przy tworzeniu SWA).

### 3. Po deployu

Azure poda URL, np. `https://datahub-vue-poc.azurewebsites.net`

## Struktura

```
vue-poc/
├── index.html              # Wejście
├── package.json            # Vue 3 + Vite
├── vite.config.js          # Konfiguracja Vite
├── staticwebapp.config.json  # Konfiguracja Azure SWA (SPA fallback)
├── src/
│   ├── main.js             # Montuje Vue
│   └── App.vue             # Wszystko w jednym komponencie
└── README.md
```
