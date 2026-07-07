# UWAGA: Gunicorn nie jest już używany.
# DataHub używa Uvicorn jako serwera ASGI.
# Konfiguracja znajduje się w startup.sh (flagi uvicorn).
# 
# Aby odpalic lokalnie:
#   uvicorn App:app --host 0.0.0.0 --port 5000 --reload
