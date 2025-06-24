#!/usr/bin/env bash

PORT=${VOICE_PORT:-8080}
NODE_ENV=${NODE_ENV:-production}

if [ ! -d "node_modules" ]; then
  npm install
fi

export VOICE_PORT="$PORT"
node human_ai_voice_server.js
