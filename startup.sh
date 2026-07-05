#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Przechodzimy do katalogu skryptu, żeby Python znalazł App.py
cd "$(dirname "$0")" || exit 1
export PYTHONPATH=$(pwd):$PYTHONPATH

# Uruchom Streamlit w tle na porcie 8501 (Flask proxy na /streamlit/)
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.enableWebsocketCompression false \
    > /tmp/streamlit.log 2>&1 &

echo "Streamlit PID: $!"

# Konfiguracja w gunicorn.conf.py
gunicorn App:app
