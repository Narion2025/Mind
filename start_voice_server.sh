#!/bin/bash

echo "==================================="
echo "🚀 Starte Human AI Voice Server..."
echo "==================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prozess auf Port 8000 automatisch beenden
PORT_IN_USE_PID=$(lsof -ti:8000)
if [ -n "$PORT_IN_USE_PID" ]; then
  echo "⚠️ Port 8000 ist belegt (PID: $PORT_IN_USE_PID). Beende Prozess..."
  kill -9 "$PORT_IN_USE_PID"
  echo "✅ Prozess $PORT_IN_USE_PID wurde beendet."
fi

# Abhängigkeiten prüfen/installieren
if [ ! -d "node_modules" ]; then
  echo "📦 node_modules nicht gefunden – führe 'npm install' aus..."
  npm install
fi

REQUIRED_MODULES=("ws" "dotenv")
for module in "${REQUIRED_MODULES[@]}"; do
  if ! npm list "$module" &>/dev/null; then
    echo "📦 '$module' wird installiert..."
    npm install "$module"
  fi
done

# Umgebungsvariablen setzen
if [ -z "$HUME_API_KEY" ]; then
  echo "Error: HUME_API_KEY environment variable is not set." >&2
  exit 1
fi
PORT=${PORT:-8080}
export PORT

# Starte den Server
echo "🎙️ Server wird gestartet auf PORT=$PORT..."
node human_ai_voice_server.js
