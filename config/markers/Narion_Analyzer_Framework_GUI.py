
#!/usr/bin/env python3
"""
Narion Analyzer Framework GUI
=============================
Ein modulares Framework zur Integration aller Marker-Cluster, inklusive:
- Marion-Phänomenanalyse
- Driftachsen
- EmotionGuard
- Spiral Dynamics
- Levelstruktur (9-Felder-System)
- Metamarker-Overlay
- Export- und Batchfunktionen
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext
import matplotlib.pyplot as plt
import yaml
import re
import os
import csv

# Basis-GUI
root = tk.Tk()
root.title("Narion Analyzer – Integriertes Framework")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

text_output = scrolledtext.ScrolledText(root, width=110, height=25)
text_output.pack(padx=10, pady=10)

loaded_text = ""

def load_text_file():
    global loaded_text
    file_path = filedialog.askopenfilename(filetypes=[("Textdateien", "*.txt")])
    if not file_path:
        return
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_text = f.read()
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, loaded_text[:3000] + "\n... (Text geladen, gekürzt für Vorschau)\n")

def export_to_csv(data, filename="narion_analysis_output.csv"):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Platzhalterfunktionen für Modul-Buttons
def run_marion_module():
    text_output.insert(tk.END, "\n[Modul: Marion-Analyse aktiviert – Implementierung folgt]\n")

def run_emotion_guard():
    text_output.insert(tk.END, "\n[Modul: EmotionGuard aktiviert – Implementierung folgt]\n")

def run_drift_analysis():
    text_output.insert(tk.END, "\n[Modul: Driftachsen aktiviert – Implementierung folgt]\n")

def run_level_matrix():
    text_output.insert(tk.END, "\n[Modul: 9-Feld-Levelsystem aktiviert – Implementierung folgt]\n")

def run_metamarker_overlay():
    text_output.insert(tk.END, "\n[Modul: Metamarker-Overlay aktiviert – Implementierung folgt]\n")

# Buttons für Modulwahl
tk.Button(frame, text="Text laden", command=load_text_file).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Marion", command=run_marion_module).grid(row=0, column=1, padx=5)
tk.Button(frame, text="EmotionGuard", command=run_emotion_guard).grid(row=0, column=2, padx=5)
tk.Button(frame, text="Drift", command=run_drift_analysis).grid(row=0, column=3, padx=5)
tk.Button(frame, text="LevelMatrix", command=run_level_matrix).grid(row=0, column=4, padx=5)
tk.Button(frame, text="MetaOverlay", command=run_metamarker_overlay).grid(row=0, column=5, padx=5)

root.mainloop()


# Erweiterung: Marion-Analyse vollständig integrieren
def run_marion_module():
    if not loaded_text:
        text_output.insert(tk.END, "\n[Bitte zuerst eine Textdatei laden]\n")
        return

    try:
        with open("Emergenzphänomen_Marion.yaml", "r", encoding="utf-8") as file:
            cluster_data = yaml.safe_load(file)["Emergenzphänomen_Marion"]["conditions"]
    except FileNotFoundError:
        text_output.insert(tk.END, "\n[Emergenzphänomen_Marion.yaml nicht gefunden]\n")
        return

    scores = {}
    text_lower = loaded_text.lower()
    for cluster, props in cluster_data.items():
        tokens = props["tokens"]
        matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        scores[cluster] = {
            "matches": matches,
            "count": len(matches),
            "total": len(tokens),
            "score": len(matches) / len(tokens)
        }

    # Ausgabe im GUI
    text_output.insert(tk.END, "\n=== Marion-Phänomenkarte ===\n")
    for cluster, data in scores.items():
        text_output.insert(tk.END, f"Cluster: {cluster}\n")
        text_output.insert(tk.END, f"  Marker gefunden: {data['matches']}\n")
        text_output.insert(tk.END, f"  Trefferanzahl: {data['count']} von {data['total']}\n")
        text_output.insert(tk.END, f"  Kohärenzgrad: {data['score']:.2f}\n")
        if data['score'] >= 0.8:
            text_output.insert(tk.END, "  ➤ Emergenzmoment erkannt!\n")
        text_output.insert(tk.END, "\n")

    # Visualisierung
    import matplotlib.pyplot as plt
    labels = list(scores.keys())
    values = [scores[k]["score"] for k in labels]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color='indigo')
    plt.title("Phänomenkarte – Resonanzfeld Marion")
    plt.ylabel("Kohärenzgrad")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Erweiterung: EmotionGuard-Modul
def run_emotion_guard():
    if not loaded_text:
        text_output.insert(tk.END, "\n[Bitte zuerst eine Textdatei laden]\n")
        return

    try:
        with open("emotion_guard.yaml", "r", encoding="utf-8") as file:
            emotion_data = yaml.safe_load(file)
    except FileNotFoundError:
        text_output.insert(tk.END, "\n[emotion_guard.yaml nicht gefunden]\n")
        return

    results = []
    text_lower = loaded_text.lower()
    for category, tokens in emotion_data.items():
        matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        score = len(matches) / len(tokens) if tokens else 0
        results.append((category, matches, len(matches), len(tokens), score))

    # GUI-Ausgabe
    text_output.insert(tk.END, "\n=== EmotionGuard Analyse ===\n")
    for category, matches, count, total, score in results:
        text_output.insert(tk.END, f"Emotionale Kategorie: {category}\n")
        text_output.insert(tk.END, f"  Marker gefunden: {matches}\n")
        text_output.insert(tk.END, f"  Trefferanzahl: {count} von {total}\n")
        text_output.insert(tk.END, f"  Emotionsintensität: {score:.2f}\n\n")

    # Visualisierung
    import matplotlib.pyplot as plt
    labels = [r[0] for r in results]
    values = [r[4] for r in results]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color='darkred')
    plt.title("EmotionGuard – Affektive Aktivierung")
    plt.ylabel("Intensität")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Erweiterung: 9-Level Spiral Dynamics Modul
def run_level_matrix():
    if not loaded_text:
        text_output.insert(tk.END, "\n[Bitte zuerst eine Textdatei laden]\n")
        return

    try:
        with open("enhanced_marker_config.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        text_output.insert(tk.END, "\n[enhanced_marker_config.txt nicht gefunden]\n")
        return

    # Struktur: jeder Level beginnt mit #
    level_map = {}
    current_level = None
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            current_level = line[1:].strip()
            level_map[current_level] = []
        elif line and current_level:
            level_map[current_level].append(line)

    results = []
    text_lower = loaded_text.lower()
    for level, tokens in level_map.items():
        matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        score = len(matches) / len(tokens) if tokens else 0
        results.append((level, matches, len(matches), len(tokens), score))

    # GUI-Ausgabe
    text_output.insert(tk.END, "\n=== Spiral Dynamics – 9-Level Matrix ===\n")
    for level, matches, count, total, score in results:
        text_output.insert(tk.END, f"Level: {level}\n")
        text_output.insert(tk.END, f"  Marker gefunden: {matches}\n")
        text_output.insert(tk.END, f"  Trefferanzahl: {count} von {total}\n")
        text_output.insert(tk.END, f"  Levelresonanz: {score:.2f}\n\n")

    # Visualisierung
    import matplotlib.pyplot as plt
    labels = [r[0] for r in results]
    values = [r[4] for r in results]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='teal')
    plt.title("Spiral Dynamics – 9-Level Resonanz")
    plt.ylabel("Resonanzwert")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Erweiterung: Driftachsenanalyse mit Richtungsbeschreibung
def run_drift_analysis():
    if not loaded_text:
        text_output.insert(tk.END, "\n[Bitte zuerst eine Textdatei laden]\n")
        return

    try:
        with open("drift_marker_axes.yaml", "r", encoding="utf-8") as file:
            drift_axes = yaml.safe_load(file)
    except FileNotFoundError:
        text_output.insert(tk.END, "\n[drift_marker_axes.yaml nicht gefunden]\n")
        return

    text_lower = loaded_text.lower()
    drift_results = []

    for axis_name, axis in drift_axes.items():
        start_tokens = axis.get("start", [])
        end_tokens = axis.get("end", [])
        transition_tokens = axis.get("transition", [])
        start_matches = [t for t in start_tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        end_matches = [t for t in end_tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        transition_matches = [t for t in transition_tokens if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]

        drift_strength = len(transition_matches) / (len(transition_tokens) or 1)
        direction = "→" if end_matches and not start_matches else "←" if start_matches and not end_matches else "↔"

        drift_results.append({
            "axis": axis_name,
            "from": start_matches,
            "to": end_matches,
            "via": transition_matches,
            "strength": drift_strength,
            "direction": direction
        })

    # GUI-Ausgabe
    text_output.insert(tk.END, "\n=== Driftachsenanalyse ===\n")
    for result in drift_results:
        text_output.insert(tk.END, f"Achse: {result['axis']} {result['direction']}\n")
        text_output.insert(tk.END, f"  Von: {result['from']}\n")
        text_output.insert(tk.END, f"  Nach: {result['to']}\n")
        text_output.insert(tk.END, f"  Übergangsmarker: {result['via']}\n")
        text_output.insert(tk.END, f"  Driftdichte: {result['strength']:.2f}\n\n")

    # Visualisierung
    import matplotlib.pyplot as plt
    labels = [r["axis"] for r in drift_results]
    values = [r["strength"] for r in drift_results]

    plt.figure(figsize=(9, 5))
    plt.bar(labels, values, color='darkblue')
    plt.title("Semantische Driftachsen – Übergangsdichte")
    plt.ylabel("Driftdichte")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Erweiterung: Metamarker-Overlay
def run_metamarker_overlay():
    if not loaded_text:
        text_output.insert(tk.END, "\n[Bitte zuerst eine Textdatei laden]\n")
        return

    try:
        with open("o3_text_markers.yaml", "r", encoding="utf-8") as file:
            overlay_markers = yaml.safe_load(file)
    except FileNotFoundError:
        text_output.insert(tk.END, "\n[o3_text_markers.yaml nicht gefunden]\n")
        return

    text_lower = loaded_text.lower()
    meta_results = []

    for overlay, token_list in overlay_markers.items():
        matches = [t for t in token_list if re.search(r"\b" + re.escape(t) + r"\b", text_lower)]
        ratio = len(matches) / len(token_list) if token_list else 0
        meta_results.append((overlay, matches, len(matches), len(token_list), ratio))

    # GUI-Ausgabe
    text_output.insert(tk.END, "\n=== MetaMarker-Overlay ===\n")
    for overlay, matches, count, total, ratio in meta_results:
        text_output.insert(tk.END, f"Metakategorie: {overlay}\n")
        text_output.insert(tk.END, f"  Marker gefunden: {matches}\n")
        text_output.insert(tk.END, f"  Anteil: {count} von {total} = {ratio:.2f}\n\n")

    # Visualisierung
    import matplotlib.pyplot as plt
    labels = [m[0] for m in meta_results]
    values = [m[4] for m in meta_results]

    plt.figure(figsize=(9, 5))
    plt.bar(labels, values, color='orange')
    plt.title("Metamarker-Overlay – Strukturfrequenz")
    plt.ylabel("Anteil der aktiven Marker")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Erweiterung: Export- und Batchfunktion
def batch_analyze_directory():
    directory = filedialog.askdirectory()
    if not directory:
        return

    summary = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().lower()

            file_results = {"Datei": filename}

            # Marion-Modul
            try:
                with open("Emergenzphänomen_Marion.yaml", "r", encoding="utf-8") as file:
                    marion_data = yaml.safe_load(file)["Emergenzphänomen_Marion"]["conditions"]
                for cluster, props in marion_data.items():
                    matches = [t for t in props["tokens"] if re.search(r"\b" + re.escape(t) + r"\b", text)]
                    file_results[f"Marion_{cluster}"] = round(len(matches) / len(props["tokens"]), 2)
            except:
                pass

            # EmotionGuard
            try:
                with open("emotion_guard.yaml", "r", encoding="utf-8") as file:
                    emo_data = yaml.safe_load(file)
                for cat, tokens in emo_data.items():
                    matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text)]
                    file_results[f"Emotion_{cat}"] = round(len(matches) / len(tokens), 2)
            except:
                pass

            # MetaOverlay
            try:
                with open("o3_text_markers.yaml", "r", encoding="utf-8") as file:
                    meta_data = yaml.safe_load(file)
                for cat, tokens in meta_data.items():
                    matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text)]
                    file_results[f"Meta_{cat}"] = round(len(matches) / len(tokens), 2)
            except:
                pass

            summary.append(file_results)

    if summary:
        export_to_csv(summary, filename="Narion_Export.csv")
        text_output.insert(tk.END, "\n[Batch-Analyse abgeschlossen – Daten gespeichert in Narion_Export.csv]\n")
    else:
        text_output.insert(tk.END, "\n[Keine passenden Textdateien im Ordner gefunden]\n")

# Button für Batch-Analyse
tk.Button(frame, text="Batch-Analyse & Export", command=batch_analyze_directory).grid(row=0, column=6, padx=5)
