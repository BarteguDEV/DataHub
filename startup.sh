#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Przechodzimy do katalogu skryptu, żeby Python znalazł App.py
cd "$(dirname "$0")" || exit 1
export PYTHONPATH=$(pwd):$PYTHONPATH

# Port Streamlit — można nadpisać zmienną środowiskową STREAMLIT_PORT
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"
echo "=== DataHub startup ==="
echo "Python: $(python --version 2>&1)"
echo "Streamlit port: $STREAMLIT_PORT"
echo "Flask port: ${PORT:-8000}"

# Uruchom Streamlit w tle na STREAMLIT_PORT (Flask proxy na /streamlit/)
echo "Starting Streamlit on port $STREAMLIT_PORT ..."
python -m streamlit run streamlit_app.py \
    --server.port "$STREAMLIT_PORT" \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.enableWebsocketCompression false \
    --browser.gatherUsageStats false \
    > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "Streamlit PID: $STREAMLIT_PID"

# Odczekaj chwilę i sprawdź czy Streamlit wystartował
sleep 3
if kill -0 $STREAMLIT_PID 2>/dev/null; then
    echo "Streamlit started successfully (PID $STREAMLIT_PID)"
else
    echo "WARNING: Streamlit process died. Check /tmp/streamlit.log for details."
    tail -20 /tmp/streamlit.log
fi

# Konfiguracja w gunicorn.conf.py + Azure App Service ustawia PORT
echo "Starting Gunicorn (Flask) on port ${PORT:-8000}..."
gunicorn App:app
