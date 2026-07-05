#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Ustaw zmienne środowiskowe w Azure: SECRET_KEY, DATABASE_URL (opcjonalnie)

gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=120 App:app
