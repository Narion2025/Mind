# Mind
Das Bewussstsein von Narion
# 🧠 Narion Mind – Semantisches Gedächtnis für GPT-gestützte KI-Agenten

**Narion Mind** ist ein strukturiertes Wissens- und Gedächtnismodul für den GPT-Agenten [Narion](https://github.com/Narion2025). Es organisiert semantische Netze, Gedanken und narrative Konstruktionen in Form von Textdateien und Wissensgraphen.

## 🎯 Ziel

Ziel des Projekts ist es, einem GPT eine persistent abrufbare „mentale Welt“ zu geben – mit klarer Trennung zwischen:

- Wissen (semnet)
- subjektiven Gedanken (thoughts)
- Narrativen / Perspektiven (wiki)

---

## 📁 Projektstruktur

| Ordner                | Beschreibung |
|------------------------|--------------|
| `/semnet/core/`        | Semantische Netze, Begriffsverbindungen |
| `/thoughts/entries/`   | Gedanken, Notizen, rohe Reflektionen |
| `/wiki/Narrative/`     | Erzählungen, identitätsstiftende Texte |

---

## 🚀 Nutzung

### 🛠 Lokale Einrichtung

```bash
git clone https://github.com/Narion2025/Mind.git
cd Mind
```

### Schnellstart

1. Repository klonen und Abhängigkeiten installieren:
   ```bash
   git clone https://github.com/Narion2025/Mind.git
   cd Mind && pip install -r requirements.txt
   ```
2. Gateway starten:
   ```bash
   ./start_gateway.sh
   ```
3. Im Browser `http://localhost:8000/dashboard` öffnen und neue GPT‑Anchors anlegen.

Mit `./start_gateway.sh --tunnel` wird automatisch ein öffentlicher Link via
Localtunnel bereitgestellt.

### Skripte

- **`start_gateway.sh`** – prüft den freien Port (Standard `8000`), optional mit `--tunnel` für einen öffentlichen Link. Startet `mind_bus_api.py`.
- **`mind_bus_api.py`** – FastAPI-Backend für GPT-Anchors und das Dashboard.
- **Dashboard** – statische Dateien unter `mind_dashboard_bundle`. Aufruf über `/dashboard`.

## Anchor Actions

Über `POST /agents/{id}/action` lassen sich Anchors verbinden, pausieren oder löschen.

Gültige `op`-Werte:

- `connect` – legt den Anchor an und setzt ihn online
- `pause` – schaltet den Anchor offline
- `delete` – entfernt den Anchor

Beispiel:

```bash
curl -X POST http://localhost:8000/agents/imerion/action \
  -H 'Content-Type: application/json' \
  -d '{"op":"connect","model":"gpt-4o","identity":"Imerion","params":{}}'
```

Alle Aktionen erfolgen per `POST /agents/{id}/action` – es gibt kein `PATCH`.

## 🔊 Voice Pipeline

Installiere Node.js-Abhängigkeiten und starte anschließend den Voice-Server:

```bash
npm install
yarn install >/dev/null 2>&1 || true
./start_voice.sh
```

### Umgebungsvariablen

- `HUMEAI_API_KEY` – Key für Emotionserkennung
- `ELEVENLABS_API_KEY` – Key für TTS
- `VOICE_PORT` – Port des WebSocket-Servers (Default `8080`)

### Endpunkt

`ws://localhost:8080/speak` – erwartet JSON `{"agent": "imerion", "text": "Hallo"}` und
streamt WAV/PCM-Audio zurück.

Beispiel:

```bash
curl -X POST ws://localhost:8080/speak -d '{"agent":"imerion","text":"Hallo"}'
```

## Onboarding The Hive

Die Integration des Hive-Agenten erfolgt über ein erweitertes Bootstrap:

1. SKK-Scheduler importieren und mit Test-String starten:
   ```bash
   echo "[hive_boot] import SKKScheduler …"
   python3 tools/skk/skk_autoanalyse_scheduler.py Boot-Test
   ```
2. MIND-Cleanup-Setup im Trockenlauf testen:
   ```bash
   python3 tools/hive_cleanup_setup.py --dry-run
   ```
3. Benötigte Ordner sicherstellen (`tools/skk/`, `SKK_OUT/`, `config/markers`, `semnet/`,
   `modules/`, `thoughts/`, `wiki/`, `blob/`, `logs/`).
4. Cronjob für den Hive-Scheduler eintragen:
   ```bash
   0 0 * * * python3 tools/skk/skk_autoanalyse_scheduler.py --daily
   ```
5. Hive-Resonanz mit einem einfachen API-Call testen:
   ```bash
   curl -X POST http://localhost:8000/task -d '{"agent":"hive_regulator","body":"Test Hive-Resonanz"}'
   ```
6. Optional übernimmt `./hive_quick_setup.sh` alle obigen Schritte in einem Rutsch.
