#!/bin/bash

ENV_PY="narion-env/bin/python3"
PORT=${API_PORT:-8000}
if lsof -i :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "Killing processes on port $PORT" >&2
  lsof -ti :$PORT -sTCP:LISTEN | xargs -r kill
  sleep 1
fi

echo "Starte Narion Agent..."
$ENV_PY narion_emotion_loop.py &

sleep 1

echo "Starte Mint Manager..."
$ENV_PY gpt_Narion/mint_manager.py &

sleep 1

echo "Starte Thought Validator..."
$ENV_PY MIND_CI_Validation/scripts/validate_thoughts.py &

sleep 1

echo "Starte Voice Server..."
./start_voice_server.sh &

echo "Initialisiere Ankerpunkt..."
echo "Pfad: init/anchors/ankerpunkt.yaml (nur manuell oder über Interface verwendbar)"

echo "Systembereit. Logs in Terminal prüfen."
