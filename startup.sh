#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Przechodzimy do katalogu skryptu, żeby Python znalazł App.py
cd "$(dirname "$0")" || exit 1
export PYTHONPATH=$(pwd):$PYTHONPATH

# Konfiguracja w gunicorn.conf.py
gunicorn App:app
