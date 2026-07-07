#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# FastAPI + Uvicorn. Streamlit startuje automatycznie jako subprocess.
set -e

cd "$(dirname "$0")" || exit 1
export PYTHONPATH=$(pwd):$PYTHONPATH

echo "=== DataHub startup (FastAPI) ==="
echo "Python: $(python --version 2>&1)"
echo "Port: ${PORT:-8000}"
echo "Streamlit port: ${STREAMLIT_PORT:-8501}"

exec uvicorn App:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1
