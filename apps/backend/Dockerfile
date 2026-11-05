#!/bin/sh

set -e

echo "=================================="
echo " Démarrage du backend"
echo "=================================="

# Appliquer les migrations Alembic
echo "[1/2] Application des migrations..."
uv run --no-sync alembic upgrade head

# Démarrer le serveur FastAPI
echo "[2/2] Démarrage de FastAPI..."
exec uv run --no-sync uvicorn \
    --app-dir src \
    main:app \
    --host 0.0.0.0 \
    --port 8000

pip install requests