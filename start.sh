#!/usr/bin/env bash
set -euo pipefail

APP_MODULE="${APP_MODULE:-app.main:app}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

if ! command -v litestar >/dev/null 2>&1; then
  echo "litestar is not installed or not available in PATH."
  echo "Run: python -m venv .venv && source .venv/bin/activate && pip install -e ."
  exit 1
fi

echo "Starting Kubernetes AI Agent at http://${HOST}:${PORT}"
exec litestar --app "${APP_MODULE}" run --reload --host "${HOST}" --port "${PORT}"
