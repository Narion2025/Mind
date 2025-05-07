#!/bin/bash

# Verzeichnisse
BASE_DIR="$HOME/Documents/GitHub/Mind"
LOG_DIR="$BASE_DIR/logs"

# Stelle sicher, dass Log-Verzeichnis existiert
mkdir -p "$LOG_DIR"

# Datums- und Zeitstempel
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/skk_analysis_$TIMESTAMP.log"

# Wechsle ins Arbeitsverzeichnis
cd "$BASE_DIR" || {
  echo "Fehler: Konnte nicht in $BASE_DIR wechseln" > "$LOG_FILE"
  exit 1
}

# Führe Analyse aus und logge Ergebnisse
echo "=== SKK-Analyse gestartet: $TIMESTAMP ===" > "$LOG_FILE"

# Führe Python-Skript aus
python skk_autoanalyse.py >> "$LOG_FILE" 2>&1

# Führe auch den System-Monitor aus
python system_monitor.py >> "$LOG_FILE" 2>&1

echo "=== SKK-Analyse beendet: $(date +"%Y-%m-%d_%H-%M-%S") ===" >> "$LOG_FILE"

# Optional: Kopiere die neuesten Log-Einträge ins System-Verzeichnis
tail -50 "$LOG_FILE" > "$BASE_DIR/Narion_MIND_Cleaned_Structure/skk/system/latest_run.log"

echo "SKK-Analyse abgeschlossen. Log: $LOG_FILE"