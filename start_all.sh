#!/bin/bash

ENV_PY="${ENV_PY:-narion-env/bin/python3}"

PORT=8000
PIDS=$(lsof -t -i :$PORT 2>/dev/null)
if [[ -n "$PIDS" ]]; then
  echo "Killing processes on port $PORT: $PIDS"
  kill $PIDS 2>/dev/null || true
  sleep 1
fi

echo "Starte Gateway..."
./mind_gateway.sh &
sleep 1

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
