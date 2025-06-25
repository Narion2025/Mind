#!/usr/bin/env bash

PORT=${PORT:-8000}
API_PORT=${API_PORT:-$PORT}
JWT_PUBLIC_KEY=${JWT_PUBLIC_KEY:-}
DATABASE_URL=${DATABASE_URL:-sqlite:///./gateway.db}

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

if lsof -i :$API_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "Error: port $API_PORT is already in use" >&2
  exit 1
fi

export PORT=$API_PORT
export JWT_PUBLIC_KEY
export DATABASE_URL

if [[ $TUNNEL -eq 1 ]]; then
  npx localtunnel --port $API_PORT &
fi

python3 mind_bus_api.py

