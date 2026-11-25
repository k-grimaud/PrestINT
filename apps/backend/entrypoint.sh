
#!/bin/sh

set -e

echo "=================================="
echo " DÃ©marrage du backend"
echo "=================================="

# Appliquer les migrations Alembic
echo "[1/2] Application des migrations..."
uv run --no-sync alembic upgrade head

# En parallÃ¨le : vÃ©rifie le dump Calend'INT au dÃ©marrage
uv run --no-sync python -m src.calendint_dump.dump_database || echo "CalendINT : vÃ©rification Ã©chouÃ©e"

# DÃ©marrer le serveur FastAPI
echo "[2/2] DÃ©marrage de FastAPI..."
exec uv run --no-sync uvicorn \
    --app-dir src \
    main:app \
    --host 0.0.0.0 \
    --port 8000 "$@"
