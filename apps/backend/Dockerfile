FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
# Splitting dependencies (local / "online") to prevent useless rebuilds
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-install-project
COPY . .
# Normalise entrypoint.sh : retire le BOM UTF-8 et les fins de ligne CRLF
RUN sed -i '1s/^\xEF\xBB\xBF//; s/\r$//' entrypoint.sh
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
EXPOSE 8000

CMD ["sh", "-c", "sed '1s/^\\xEF\\xBB\\xBF//; s/\\r$//' entrypoint.sh > /tmp/entrypoint.sh && sh /tmp/entrypoint.sh --reload"]
