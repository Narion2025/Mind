#!/usr/bin/env python3
"""
Boot-Loader für das MIND-System.
Wird als erstes Kommando im Container/Procfile aufgerufen.
"""
import os, subprocess, yaml, json, pathlib, time
from datetime import datetime

ROOT = pathlib.Path(os.getenv("MIND_ANCHOR", "~/mind_root")).expanduser()
FIRST_RUN_FLAG = ROOT / ".first_run_done"

def run_shell_setup():
    print("🧠 Erst-Setup wird ausgeführt …")
    subprocess.run(["bash", "mind_reactivation.sh"], check=True)
    FIRST_RUN_FLAG.touch()

def load_persona():
    core = ROOT / "MIND/persona/core.yaml"
    if not core.exists():
        print("⚠️ Keine persona/core.yaml – vermutlich Erst-Run.")
        run_shell_setup()
    with open(core, "r") as f:
        persona = yaml.safe_load(f)
    print(f"👤 Persona geladen: {persona['agent_name']}")
    return persona

def warmstart_vecstore():
    vec_path = ROOT / "MIND/semnet/vecstore/index.faiss"
    if vec_path.exists():
        print("🔎 Vector-Index geladen.")
    else:
        print("🔎 Kein Vector-Index gefunden – wird beim nächtlichen Rebuild erzeugt.")

def start_cron_jobs():
    print("⏲️ Cron/Watchdog wird gestartet …")
    # Beispiel: subprocess.Popen([...]) oder System-Cron nutzen
    # → hier nur Platzhalter
    time.sleep(0.1)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    persona = load_persona()
    warmstart_vecstore()
    start_cron_jobs()
    print("✅ Boot-Sequenz abgeschlossen – Agent bereit.")

if __name__ == "__main__":
    main()
