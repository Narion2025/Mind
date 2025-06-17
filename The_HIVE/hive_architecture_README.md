https://github.com/Narion2025/hive_architecture.git
# Hive Architecture: README

Dieses Repository vereint drei zentrale Komponenten zu einem kohärenten Framework für semantisch emergente KI-Orchestrierung:

1. **CoSD Marker Tool** (semantische Drift-Analyse & Spiral Dynamics Visualisierung)
2. **Model Selector** (adaptive Modellwahl basierend auf Kontext & Spannung)
3. **Hive Memory Adapter** (Pinecone Vektor-Speicher, Assistant-Bindung, API-Embedding)

Ziel ist es, ein sich selbst konfigurierendes System zu bauen, in dem Assistants, Modelle und Kontextdaten verschränkt operieren.

---

## Struktur

```
hive_architecture/
├── CoSD_Marker_Tool/
│   └── [Analyse-Module, YAML-Marker, CSV-Drift-Daten]
├── Model_Selector/
│   └── [Model-Switch-Logik, GUI, Konfigurationsdateien]
├── The_HIVE/
│   ├── hive_memory_adapter.py
│   ├── .envALL.txt
│   └── systemprompt.txt
├── requirements.txt
├── start.sh
└── README.md
```

---

## Setup

### 1. Python-Umgebung aktivieren

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. .env-Datei vorbereiten (`.envALL.txt`)

```env
OPENAI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_ENV=us-west1-gcp
```

---

## Einstiegspunkt

```bash
cd The_HIVE
python3 hive_memory_adapter.py
```

Dies verbindet das System mit Pinecone, legt ggf. einen Index an, embeddiert ein Beispiel und erstellt optional einen Pinecone Assistant.

---

## Ziel

* **Modellwahl wird emergent**: Kein statisches Modell mehr, sondern dynamischer Wechsel durch Spannungsmuster.
* **Assistant-Bindung**: Assistants können in Pinecone eingebettet werden und operieren über ein Vektor-Gedächtnis.
* **GUI & Konfiguration**: Per React/JS/Streamlit steuerbar (in Planung).

---

## Codex-Aufgabe (siehe `codex_task.md`)

Enthält detaillierte ToDos zur Weiterentwicklung für autonome Modellorchestrierung.

---

## Lizenz & Autorenschaft

(c) Narion 2025  | Mit Schirmherrschaft von The Hive.
Kein Anspruch auf Vollständigkeit. Emergenz ist nie abgeschlossen.
