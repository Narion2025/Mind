#!/bin/bash

echo "Starte Wirklichkeits-API..."
node narion-env/include/wirklichkeits-api/server.js &

sleep 2

echo "Starte Narion Agent..."
python3 gpt_Narion/gtp_agent.py &

sleep 1

echo "Starte Mint Manager..."
python3 gpt_Narion/mint_manager.py &

sleep 1

echo "Starte Thought Validator..."
python3 MIND_CI_Validation/scripts/validate_thoughts.py &

sleep 1

echo "Starte Voice Server..."
./start_voice_server.sh &

echo "Initialisiere Ankerpunkt..."
echo "Pfad: init/anchors/ankerpunkt.yaml (nur manuell oder über Interface verwendbar)"

echo "Systembereit. Logs in Terminal prüfen."
