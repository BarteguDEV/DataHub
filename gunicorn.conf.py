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
worker_class = "sync"
log_file = "-"
