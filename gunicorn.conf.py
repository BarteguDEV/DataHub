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

# UWAGA — Azure App Service (dla WebSocket Streamlit):
#
# Aby WebSocket Streamlit działał poprawnie, wymagane są:
#
# 1. **Azure Portal → App Service → Configuration → General Settings**
#    - "Web sockets" = **ON** (domyślnie wyłączone!)
#    - "Always On" = **ON** (zapobiega usypianiu procesów)
#
# 2. **Zmienne środowiskowe (Application Settings)**:
#    - STREAMLIT_PORT=8501  (można zmienić jeśli 8501 jest zajęty)
#
# 3. **startup.sh** uruchamia Streamlit w tle na STREAMLIT_PORT,
#    a Flask proxy przekierowuje /streamlit/ → localhost:8501
#
# Test WebSocket w Azure:
#   curl -v -H "Connection: Upgrade" -H "Upgrade: websocket" \
#     https://twoja-aplikacja.azurewebsites.net/_stcore/health
