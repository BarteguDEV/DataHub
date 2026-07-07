"""Konfiguracja Gunicorn — automatycznie odczytana przez `gunicorn App:app`."""

import multiprocessing
import os

# Azure App Service ustawia PORT dynamicznie — używamy go z fallbackiem
port = os.getenv("PORT", 8000)
bind = f"0.0.0.0:{port}"
workers = (multiprocessing.cpu_count() * 2) + 1
timeout = 120
max_requests = 1000
max_requests_jitter = 50
worker_class = "gevent"
log_file = "-"

# Aby module-level code (Streamlit subprocess) odpalił się tylko w masterze,
# a nie w każdym workerze z osobna.
preload_app = True

# UWAGA — Streamlit w Azure App Service (Linux):
#
# Streamlit jest uruchamiany automatycznie przez App.py jako subprocess OS
# (subprocess.Popen) przy starcie gunicorna. Żaden dodatkowy skrypt nie jest
# potrzebny — preload_app=True gwarantuje, że odpali się tylko raz w masterze.
#
# Kluczowe ustawienia Azure:
#
# 1. **App Service → Configuration → General Settings**
#    - "Web sockets" = **ON** (bez tego WebSocket Streamlit nie działa!)
#    - "Always On" = **ON** (zapobiega garbage collect)
#
# 2. **Zmienne środowiskowe (Application Settings)**:
#    - STREAMLIT_PORT=8501  (można zmienić jeśli port zajęty)
#
# Diagnostyka:
#   - Logi Streamlit: /tmp/streamlit.log (jeśli przekierujesz stdout/stderr)
#   - Test WebSocket: curl -v -H "Connection: Upgrade" \
#       -H "Upgrade: websocket" \
#       https://twoja-app.azurewebsites.net/_stcore/health
