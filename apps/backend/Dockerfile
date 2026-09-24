FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Splitting dependencies (local / "online") to prevent useless rebuilds
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "--no-sync", uvicorn","src/main:app","--host","0.0.0.0"]
