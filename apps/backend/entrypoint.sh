
#!/bin/sh

set -e

echo "=================================="
echo " Démarrage du backend"
echo "=================================="

# Appliquer les migrations Alembic
echo "[1/2] Application des migrations..."
uv run --no-sync alembic upgrade head

# En parallèle : vérifie le dump Calend'INT au démarrage
uv run --no-sync python -m src.calendint_dump.dump_database || echo "CalendINT : vérification échouée"

# Démarrer le serveur FastAPI
echo "[2/2] Démarrage de FastAPI..."
exec uv run --no-sync uvicorn \
    --app-dir src \
    main:app \
    --host 0.0.0.0 \
    --port 8000 "$@"
