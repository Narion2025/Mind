#!/usr/bin/env bash

PORT=${PORT:-8000}
API_PORT=${API_PORT:-$PORT}

PIDS=$(lsof -t -i :$API_PORT 2>/dev/null)
if [[ -n "$PIDS" ]]; then
  echo "Killing processes on port $API_PORT: $PIDS"
  kill $PIDS 2>/dev/null || true
  sleep 1
fi

exec ./start_gateway.sh "$@"
