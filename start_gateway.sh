#!/usr/bin/env bash

PORT=${PORT:-8000}
API_PORT=${API_PORT:-$PORT}
JWT_PUBLIC_KEY=${JWT_PUBLIC_KEY:-}

function usage() {
  echo "Usage: $0 [--tunnel]" >&2
  exit 1
}

TUNNEL=0
if [[ $1 == "--tunnel" ]]; then
  TUNNEL=1
elif [[ -n $1 ]]; then
  usage
fi

PIDS=$(lsof -t -i :$API_PORT 2>/dev/null)
if [[ -n "$PIDS" ]]; then
  echo "Killing processes on port $API_PORT: $PIDS"
  kill $PIDS 2>/dev/null || true
  sleep 1
fi

export PORT=$API_PORT
export JWT_PUBLIC_KEY

if [[ $TUNNEL -eq 1 ]]; then
  npx localtunnel --port $API_PORT &
fi

python3 mind_bus_api.py

