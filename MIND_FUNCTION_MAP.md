## Gruppe: Agenten

### Datei: narion_emotion_loop.py
Funktionen: read_last_emotion(), modulate_prompt(), get_gpt_response(), speak_text(), agent_loop()
Status: ⚠️ benötigt OPENAI_API_KEY und ELEVENLABS_API_KEY

### Datei: gpt_Narion/mint_manager.py
Funktion: save_to_mint(date, memory_content, insights, personality_note)
Status: ✅

### Datei: emotions_reactor.py
Funktion: generate_narion_prompt(emotions)
Status: ✅

---

## Gruppe: System

### Datei: mind_bootstrap.py
Funktionen: get_anchor(), ensure_directories(), start_scheduler_stub(), main()
Status: ✅

### Datei: system_monitor.py
Funktionen: load_yaml(), save_yaml(), update_history(), generate_report(), main()
Status: ✅

### Datei: token_registry.py
Funktionen: generate_env_files(), load_agent_env(), get_env_var()
Status: ✅

---

## Gruppe: Voice

### Datei: voice_pipeline/pipeline_orchestrator.py
Funktionen: resolve_voice(), run_pipeline(), main()
Status: ⚠️ benötigt HUMEAI_API_KEY und ELEVENLABS_API_KEY

### Datei: voice_pipeline/hume_client.py
Funktionen: __init__(), analyze()
Status: ⚠️ benötigt HUMEAI_API_KEY

### Datei: voice_pipeline/elevenlabs_tts.py
Funktionen: __init__(), synthesize()
Status: ⚠️ benötigt ELEVENLABS_API_KEY

### Datei: voice_pipeline/audio_listener.py
Funktion: listen(uri)
Status: ✅

### Datei: emotion_recognition.py
Funktionen: start_emotion_stream()
Status: ⚠️ benötigt HUME_API_KEY und Mikrofonzugriff

### Datei: emotion_recognition_sounddevice.py
Funktionen: start_emotion_stream()
Status: ⚠️ benötigt HUME_API_KEY und Sounddevice

---

## Gruppe: Bus / Kommunikation

### Datei: mind_bus_api.py
Funktionen: upsert_anchor(), list_anchors(), get_state(), health(), agent_action(), start()
Status: ✅

### Datei: wirklichkeits-api/gateway.py
Funktionen: verify_jwt(), require_role(), save_anchor(), load_anchor(), upsert_anchor(), get_anchor(), patch_anchor(), get_state(), ws_state()
Status: ⚠️ benötigt JWT_PUBLIC_KEY

### Datei: human_ai_voice_server.js
Startet WebSocket-Server auf /speak
Status: ✅

### Datei: server.js
Express-Server für Dashboard
Status: ✅

---

## Gruppe: Deployment / Tunnel / PM2

### Datei: start_gateway.sh
Startet mind_bus_api.py, optional mit LocalTunnel
Status: ✅

### Datei: start_voice_server.sh
Startet human_ai_voice_server.js
Status: ✅

### Datei: start_all.sh
Startet verschiedene Komponenten (narion_emotion_loop, mint_manager, validate_thoughts, voice server)
Status: ✅

### Datei: icebreaker.sh
Installiert pm2 und localtunnel, startet Server und Tunnel
Status: ✅

---

## Gruppe: Tests / Diagnostik

### Datei: tests/test_gateway_api.py
Enthält Integrationstests für mind_bus_api
Status: ✅

### Datei: tests/test_pipeline.py
Testet voice_pipeline
Status: ✅

### Datei: tests/e2e_register_anchor.py
End-to-End Test für Anchor-Registrierung
Status: ✅

### Datei: MIND_CI_Validation/scripts/validate_thoughts.py
Validiert Gedanken-Dateien gegen Schema
Status: ⚠️ benötigt PyYAML und jsonschema

### Datei: system_monitor.py
Siehe System-Gruppe
Status: ✅

###MIND-MAP-DONE###
