import yaml
import re
import os
from datetime import datetime

# Optional: Zusatzklassifikatoren
flugel_patterns = []  # Kann vom Scheduler ergänzt werden

# Klassifizierungseinheit
def classify_entry(text: str):
    """Klassifiziere einen Textelement."""
    if any(re.search(p, text, re.IGNORECASE) for p in flugel_patterns):
        return "flugel", "match_fly"
    if "knoten" in text.lower():
        return "knoten", "keyword_match"
    if "strudel" in text.lower():
        return "strudel", "keyword_match"
    if "kristall" in text.lower():
        return "kristall", "keyword_match"
    return "unclassified", "none"

# Hauptanalysefunktion
def run_analysis():
    print("🧠 Starte SKK-Analyse...")

    input_file = "narion_chatlog.txt"
    output_file = f"chat_analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    if not os.path.exists(input_file):
        print(f"❌ Eingabedatei '{input_file}' nicht gefunden.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = []
    for line in lines:
        label, reason = classify_entry(line)
        results.append({
            "text": line.strip(),
            "label": label,
            "reason": reason
        })

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(results, f, allow_unicode=True)

    print(f"✅ Analyse abgeschlossen. Ergebnisse in '{output_file}' gespeichert.")
