#!/bin/bash

ENV_PY="narion-env/bin/python3"

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
