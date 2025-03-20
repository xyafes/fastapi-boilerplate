FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/etc/apk/cache \
    apk update && apk add gcc musl-dev libpq-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --extra prod

COPY . .

FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apk update && apk add --no-cache libpq libmagic tini
RUN addgroup -S fastapi && adduser -S fastapi -G fastapi --disabled-password

COPY --from=builder --chown=fastapi:fastapi /app /app

RUN mkdir -p /opt/logs/
RUN chown -R fastapi:fastapi /opt/logs/

USER fastapi
ENTRYPOINT ["/sbin/tini", "--"]