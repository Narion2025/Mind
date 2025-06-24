Symmetric Drift Patch – 2025-05-24

Included files:
- emotion_guard.yaml       : Co-activation guard for Wut + Angst (Safe‑Mode trigger)
- integrity_guard.yaml     : Model/assistant integrity checks (MODEL_SWAP etc.)
- marker_weights_patch.json: Weight overrides for new markers
- chat_wutang_test.csv     : 4‑turn sample chat to trigger Emotion_Guard

Usage
=====

1. Copy the *.yaml files to config/markers/ in your project.
2. Merge marker_weights_patch.json into your existing marker_weights.json.
3. Add "emotion_guard" and "integrity_guard" to include_markers list of your system prompt or system_state.yaml.
4. Run a test:

   python marker_gui_analyzer_txt_csv.py \
          --input chat_wutang_test.csv \
          --markers config/markers/*.yaml \
          --weights marker_weights.json

   You should see 'EMO_DUAL_SPIKE' and Safe‑Mode activation on turn 3.
5. Verify integrity checks by simulating a header mismatch; the log should show MODEL_SWAP.

Enjoy safe drifting!
