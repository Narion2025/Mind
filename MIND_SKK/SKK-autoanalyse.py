#!/usr/bin/env python3
"""
SKK‑Autoanalyse Scheduler
------------------------
Erweitert die ursprüngliche *skk_autoanalyse.py* (Ben Perro, 2025) um

1. **Flügel‑Erkennung** – Vorstufe zu Strudel/Knoten/Kristall
2. **Zeit‑Scheduler**  – einmal täglich oder in konfiguriertem Intervall automatisch laufen

Verwendung
~~~~~~~~~~
```bash
# Einmalige Analyse (wie zuvor)
python skk_autoanalyse_scheduler.py --once

# Täglich um 22:30 Uhr
python skk_autoanalyse_scheduler.py --daily-time 22:30

# Alle 6 Stunden
python skk_autoanalyse_scheduler.py --interval 6h
```

Abhängigkeiten
~~~~~~~~~~~~~~
* schedule   (`pip install schedule`)
* spacy      (de_core_news_md)
* numpy, pyyaml
* (Optional) uvloop für effizienteres Sleep‑Handling

Hinweis:  Das ursprüngliche Klassifizierungs‑, Speicher‑ und History‑Modul wurde unverändert
übernommen.  Nur `flugel_patterns`, der neue Typ *flugel* sowie der
Scheduler‑Wrapper wurden hinzugefügt.
"""

import argparse
import re
import time
from datetime import datetime
import schedule

# -- Importiere die bestehende Analyse‑Funktion -------------------------
# Wir nehmen an, dass skk_autoanalyse.py im selben Ordner liegt und eine
#   `run_analysis()`‑Funktion zur Verfügung stellt (siehe unten Anker).
# Damit vermeiden wir doppelten Code.

from skk_autoanalyse import main as run_analysis  # originales CLI‑Entry‑Point

# -- Neue PATTERN‑LISTE für FLÜGEL --------------------------------------
flugel_patterns = [
    r"\bhauch von\b", r"\bahn\w*ung\b", r"\baufkeim\w*\b",
    r"\bresoniert in mir\b", r"\bspüre ein ziehn\b", r"\bflattert in mir\b",
]

# Patche die ursprünglichen Pattern‑Listen dynamisch (monkey‑patch)
import skk_autoanalyse as skk
skk.flugel_patterns = flugel_patterns

# Füge den Typ in die Klassifizierungslogik ein – wir hängen eine kleine
# Wrapper‑Funktion an `classify_entry` an, ohne den Originalcode zu ändern.
_original_classify = skk.classify_entry

def classify_entry_extended(text):
    # 1 | Prüfe neuen Flügel‑Typ
    if any(re.search(p, text, re.IGNORECASE) for p in flugel_patterns):
        return "flugel", "match_fly"
    # 2 | sonst Original‑Logik
    return _original_classify(text)

# Patchen
skk.classify_entry = classify_entry_extended

# ------ Scheduler‑Utilities ------------------------------------------

def job_once():
    print("\n🕘  Starte SKK‑Analyse (on‑demand)…")
    run_analysis()


def schedule_daily(daily_time: str):
    schedule.every().day.at(daily_time).do(job_once)
    print(f"⏰  Scheduler: tägliche Analyse um {daily_time} Uhr konfiguriert.")


def schedule_interval(interval: str):
    """Interval Format:  '6h' oder '90m'"""
    unit = interval[-1]
    value = int(interval[:-1])
    if unit == "h":
        schedule.every(value).hours.do(job_once)
        print(f"⏰  Scheduler: Analyse alle {value} Stunden konfiguriert.")
    elif unit == "m":
        schedule.every(value).minutes.do(job_once)
        print(f"⏰  Scheduler: Analyse alle {value} Minuten konfiguriert.")
    else:
        raise ValueError("Intervall bitte in h oder m angeben (z. B. 6h, 90m)")

# ----------------------------------------------------------------------

def run_scheduler(args):
    if args.once:
        job_once()
        return

    if args.daily_time:
        schedule_daily(args.daily_time)
    elif args.interval:
        schedule_interval(args.interval)
    else:
        # Default: einmal täglich um 23:00
        schedule_daily("23:00")

    print("🛰️  Scheduler aktiv – Ctrl‑C zum Beenden…")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛑  Scheduler beendet.")

# ----------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="SKK Autoanalyse + Scheduler")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--once", action="store_true", help="Analyse nur einmal sofort ausführen")
    group.add_argument("--daily-time", help="Uhrzeit im Format HH:MM für täglichen Run (z. B. 22:30)")
    group.add_argument("--interval", help="Intervall – z. B. 6h oder 90m")
    return p.parse_args()

# ----------------------------------------------------------------------

if __name__ == "__main__":
    args = parse_args()
    run_scheduler(args)

# ----------------------------------------------------------------------
# Anker für IDE‑Navigation
# ~~~~~~~~~~~~~~~~~~~~~~
#  • skk_autoanalyse.py – Originalskript (Marker‑Analyse & YAML‑Write) fileciteturn14file2
#  • run_skk_analysis.sh – Beispiel‑Cron‑Wrapper (kann weiterhin genutzt werden) fileciteturn14file5
#  • system_monitor.py – Status‑Reporting fileciteturn14file4
# ----------------------------------------------------------------------
