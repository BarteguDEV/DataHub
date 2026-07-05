#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Konfiguracja w gunicorn.conf.py

gunicorn App:app
