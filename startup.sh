#!/bin/bash
# Skrypt uruchomieniowy dla Azure App Service (Linux)
# Streamlit jest uruchamiany automatycznie przez App.py jako subprocess.
set -e

cd "$(dirname "$0")" || exit 1
export PYTHONPATH=$(pwd):$PYTHONPATH

echo "=== DataHub startup ==="
echo "Python: $(python --version 2>&1)"
echo "Flask port: ${PORT:-8000}"
echo "Streamlit port: ${STREAMLIT_PORT:-8501}"

# Gunicorn uruchamia Flask, który automatycznie odpali Streamlit jako subproces
exec gunicorn App:app
