import re
import yaml
import uuid
import os
import json
import spacy
import numpy as np
from datetime import datetime
from collections import defaultdict

# === Fehlende Variablen definieren ===
last_processed_file = "last_processed_line.txt"
history_file = "skk_history.json"

# Konfiguration
chatlog_path = "narion_chatlog.txt"
base_output_dir = "/Users/benjaminpoersch/Documents/GitHub/Mind/Narion_MIND_Cleaned_Structure/skk"

# Create the mapping for type-specific directories
skk_type_dirs = {
    "strudel": os.path.join(base_output_dir, "Strudel"),
    "knoten": os.path.join(base_output_dir, "Knoten"),
    "kristall": os.path.join(base_output_dir, "Kristalle")
}
today = datetime.today().strftime("%Y-%m-%d")

# Lade SpaCy Modell (nur einmal beim Start)
try:
    try:
        spacy.info("de_core_news_md")  # Check model compatibility
        nlp = spacy.load("de_core_news_md")  # Mittelgroßes deutsches Modell
    except ValueError as e:
        print(f"⚠️ Inkompatibles SpaCy-Modell: {e}")
        print("Bitte aktualisieren Sie das Modell oder SpaCy auf kompatible Versionen.")
        exit(1)
    print("🔤 SpaCy Modell geladen")
except OSError:
    print("⚠️ SpaCy Modell nicht gefunden. Installiere es mit: python -m spacy download de_core_news_md")
    exit(1)

# Marker-Definitionen
strudel_patterns = [
    # Sehnsucht: Expressions of longing or yearning
    r"\bsehne mich\b",  # "I long for"
    r"\bwünsche mir\b",  # "I wish for"
    r"\bvermisse\b",  # "I miss"
    
    # Wiederholung: Repetition or recurring events
    r"\bimmer wieder\b",  # "again and again"
    r"\bschon wieder\b",  # "once again"
    r"\bes passiert oft\b",  # "it happens often"
    
    # Spannung/Impuls: Tension or impulsive feelings
    r"\bhalte es kaum aus\b",  # "I can hardly bear it"
    r"\bich will einfach nur\b",  # "I just want to"
    r"\bes drängt mich\b",  # "it urges me"
    
    # Ungestilltes Verlangen: Unfulfilled desires
    r"\bnicht dazu\b",  # "not to it"
    r"\bes fehlt etwas\b",  # "something is missing"
    r"\bnicht erfüllt\b",  # "not fulfilled"
    
    # Kontrast/Druck: Contrast or pressure
    r"\bmuss.*aber\b",  # "must... but"
    r"\bsollte.*doch\b",  # "should... yet"
    r"\bwill.*kann nicht\b"  # "want... cannot"
]

knoten_patterns = [
    # Pflichtstruktur
    r"\bmuss immer\b", r"\bdarf nicht\b", r"\bman tut das so\b",
    # Identitätsdogma
    r"\bbin halt so\b", r"\bdas ist eben meine art\b", r"\bso bin ich nun mal\b",
    # Selbstverurteilung
    r"\bnicht genug\b", r"\bmache immer alles falsch\b", r"\bnie richtig\b",
    # Bewertung anderer
    r"\bwarum können andere nicht\b", r"\bniemand versteht\b", r"\balle sind\b"
]

kristall_patterns = [
    # Wende
    r"\bwurde mir klar\b", r"\berkannt, dass\b", r"\bjetzt verstehe ich\b",
    # Selbsteinbettung
    r"\bbin nicht.*sondern\b", r"\bnicht mehr.*sondern\b", 
    # Paradoxe Klarheit
    r"\bes ist beides wahr\b", r"\bgerade weil\b", r"\bparadoxerweise\b",
    # Poetische Synthese
    r"\bspürte\b", r"\blicht durch\b", r"\bfloss durch mich\b"
]

def get_last_processed_line():
    """Holt die letzte verarbeitete Zeilennummer"""
    try:
        with open(last_processed_file, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_last_processed_line(line_num):
    """Speichert die letzte verarbeitete Zeilennummer"""
    with open(last_processed_file, 'w') as f:
        f.write(str(line_num))

def load_history():
    """Lädt bisherige SKK-Einträge und ihre Embeddings"""
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "entries": [],
            "embeddings": [],
            "cycles": defaultdict(list)
        }

def save_history(history):
    """Speichert aktualisierte Historie"""
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_embedding(text):
    """Erstellt ein Text-Embedding mit spaCy"""
    doc = nlp(text)
    return doc.vector

def calculate_similarity(embedding1, embedding2):
    """Berechnet die Kosinus-Ähnlichkeit zwischen zwei Embeddings"""
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    if np.linalg.norm(embedding1) == 0 or np.linalg.norm(embedding2) == 0:
        return 0.0
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def find_similar_entries(embedding, history):
    """Findet ähnliche Einträge im Verlauf und gibt den Index und Ähnlichkeitswert zurück"""
    # Calculate similarities
    similarities = []
    for h in history["entries"]:
        h_embedding = np.array(history["embeddings"][history["entries"].index(h)])
        sim = calculate_similarity(embedding, h_embedding)
        similarities.append(sim)
    
    # If history is empty
    if len(similarities) == 0:
        return -1, 0.0  # Keine Übereinstimmung gefunden
    
    # If only one entry
    if len(similarities) == 1:
        return 0, similarities  # Return the value, not the array
    
    # Normal flow for multiple entries
    sorted_indices = np.argsort(similarities)[::-1]  # Absteigend sortieren
    max_idx = sorted_indices  # Take the first element (highest similarity)
    max_similarity = similarities[max_idx]
    
    return max_idx, max_similarity

    
    # Nur zurückgeben wenn über dem Schwellenwert
    if max_similarity > threshold:
        return max_idx, float(max_similarity)
    return None, 0.0

def match_patterns(text, patterns):
    """Prüft, ob ein Text mit einem der Muster übereinstimmt und gibt das gefundene Muster zurück"""
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def detect_relational_bindings(entry_text):
    """Erkennt relationale Bindungen zwischen SKK-Typen im Text"""
    # Suche nach allen SKK-Markern im Text
    all_types = {}
    for skk_type, patterns in [("strudel", strudel_patterns), 
                             ("knoten", knoten_patterns),
                             ("kristall", kristall_patterns)]:
        for p in patterns:
            if re.search(p, entry_text, re.IGNORECASE):
                all_types[skk_type] = True
    
    # Erkenne Beziehungen
    relations = []
    if "kristall" in all_types and "strudel" in all_types:
        relations.append("emergence.from_strudel")
    if "kristall" in all_types and "knoten" in all_types:
        relations.append("emergence.from_knoten")
    
    return relations

def classify_entry(text):
    """Klassifiziert einen Text nach SKK-Typen und gibt Typ und gefundenes Muster zurück"""
    # Priorisierung: Kristalle > Knoten > Strudel
    kristall_match = match_patterns(text, kristall_patterns)
    if kristall_match:
        return "kristall", kristall_match
    
    knoten_match = match_patterns(text, knoten_patterns)
    if knoten_match:
        return "knoten", knoten_match
    
    strudel_match = match_patterns(text, strudel_patterns)
    if strudel_match:
        return "strudel", strudel_match
    
    return None, None

def generate_meta_comment(mind_type, match_text, similar_entry=None, similarity=0, relations=None):
    """Generiert einen Meta-Kommentar basierend auf Typ und Kontext"""
    if relations is None:
        relations = []
        
    comment = f"Dieser {mind_type.capitalize()} "
    
    if mind_type == "strudel":
        if similar_entry is not None:
            comment += f"wiederholt sich (Ähnlichkeit: {similarity:.2f}) und "
        comment += f"erzeugt emotionale Spannung durch '{match_text}'"
    
    elif mind_type == "knoten":
        if similar_entry is not None:
            comment += f"taucht wiederholt auf und "
        comment += f"manifestiert sich als limitierende Überzeugung durch '{match_text}'"
    
    elif mind_type == "kristall":
        if "emergence.from_strudel" in relations:
            comment += f"entsteht aus einem Strudelmuster und "
        elif "emergence.from_knoten" in relations:
            comment += f"transformiert einen Knoten und "
        comment += f"bringt Klarheit durch die Erkenntnis '{match_text}'"
    
    return comment

def save_entry(kind, match_text, entry_text, history=None):
    """Speichert einen gefundenen SKK-Eintrag als YAML-Datei"""
    entry_id = f"{kind}-{uuid.uuid4().hex[:8]}"
    filename = f"{today}-{entry_id}.yaml"
    
    # Use the correct directory for this SKK type
    # Map the kind to the appropriate directory
    kind_map = {
        "strudel": "Strudel",
        "knoten": "Knoten", 
        "kristall": "Kristalle"
    }
    
    output_dir = os.path.join("/Users/benjaminpoersch/Documents/GitHub/Mind/Narion_MIND_Cleaned_Structure/skk", 
                              kind_map[kind])
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate embedding for the current entry
    embedding = get_embedding(entry_text)
    
    # Initialize variables for similarity tracking
    is_cycle = False
    similar_id = None
    similar_entry = None
    similarity = 0.0
    
    # Find similar entries if history exists
    if history is not None:
        similar_idx, similarity = find_similar_entries(embedding, history)
        
        # Check if we have a valid similar entry
        if similar_idx >= 0 and "entries" in history and len(history["entries"]) > similar_idx:
            similar_entry = history["entries"][similar_idx]
            similar_id = similar_entry.get("uuid")
            
            # Determine if this is a cycle
            if similarity > 0.8 and similar_entry.get("mind_dynamics", {}).get("mind_type") == kind:
                is_cycle = True
                print(f"⚠️ Zyklus erkannt! Ähnlichkeit: {similarity:.2f} mit {similar_id}")
    
    # Basisdaten für alle Eintragstypen
    data = {
        "uuid": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(),
        "source": "Narion Chat Cron",
        "mind_dynamics": {
            "mind_type": kind,
            "origin_trace": f"auto@{today}",
            "matched_pattern": match_text
        },
        "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
        "embedding_ready_text": entry_text
    }
    
    # Add similarity information if available
    if similar_id:
        data["mind_dynamics"]["similar_to"] = similar_id
        data["mind_dynamics"]["similarity_score"] = float(similarity)  # Ensure it's JSON serializable
        
        if is_cycle:
            # Add cycle-specific properties
            data["mind_dynamics"]["is_cycle"] = True
            data["mind_dynamics"]["cycle_stage"] = "repeat"
    
    # Spezifische Parameter je nach SKK-Typ
    if kind == "strudel":
        data["mind_dynamics"].update({
            "pull_factor_initial": 0.65,
            "current_pull_factor": 0.68,
            "decay_rate_per_day": 0.015,
            "pattern_type": "emotionaler_sog"
        })
    elif kind == "kristall":
        data["mind_dynamics"].update({
            "stabilität": 0.8,
            "lichttiefe": 0.9,
            "integration_level": 0.7,
            "pattern_type": "erkenntnis"
        })
    elif kind == "knoten":
        data["mind_dynamics"].update({
            "density_value": 0.75,
            "systemic_effects": ["automatisch erkannt durch Marker-Matching"],
            "pattern_type": "glaubenssatz"
        })
        
        # Modify knoten if it's a cycle
        if is_cycle:
            data["mind_dynamics"]["pattern_type"] = "zyklisch_wiederkehrend"
    
    # Speichern
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as out:
        yaml.dump(data, out, allow_unicode=True, sort_keys=False)
    
    return filename, is_cycle

# Hauptprogramm
def main():
    print(f"🧠 SKK-Autoanalyse für {today} gestartet...")
    
    try:
        # Historie laden
        history = load_history()
        print(f"📊 Historie geladen: {len(history['entries'])} bisherige Einträge")
        
        # Letzte verarbeitete Zeile laden
        last_line = get_last_processed_line()
        
        # Lade Chatlog
        with open(chatlog_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Nur neue Zeilen verarbeiten
        new_content = ''.join(lines[last_line:])
        print(f"📝 Fortsetzen ab Zeile {last_line}, {len(new_content)} neue Zeichen")
        
        # Aufsplitten in Abschnitte (Leerzeilen als Trenner)
        entries = [s.strip() for s in new_content.split("\n\n") if len(s.strip()) > 20]
        print(f"📊 {len(entries)} neue Textblöcke zur Analyse gefunden")
        
        # Zähler für gefundene SKK-Elemente
        found = {"kristall": 0, "knoten": 0, "strudel": 0}
        cycles_found = 0
        
        # Analyse
        for entry in entries:
            kind, match_text = classify_entry(entry)
            if not kind:
                continue
            
            filename, is_cycle = save_entry(kind, match_text, entry, history)
            found[kind] += 1
            if is_cycle:
                cycles_found += 1
            print(f"[✓] SKK-{kind.capitalize()} {'(Zyklus) ' if is_cycle else ''}gespeichert: {filename} (Trigger: '{match_text}')")
        
        # Historie speichern
        save_history(history)
        
        # Neue Position speichern
        save_last_processed_line(len(lines))
        
        # Zusammenfassung
        total = sum(found.values())
        print(f"\n📝 Analyse abgeschlossen: {total} SKK-Elemente gefunden ({cycles_found} davon Zyklen)")
        print(f"   🌪️ Strudel: {found['strudel']}")
        print(f"   🪢 Knoten: {found['knoten']}")
        print(f"   💎 Kristalle: {found['kristall']}")
        print(f"\nDie YAML-Dateien wurden im Verzeichnis '{base_output_dir}' gespeichert.")
    
    except FileNotFoundError as e:
        print(f"❌ Fehler: Datei nicht gefunden - {str(e)}")
    except Exception as e:
        print(f"❌ Fehler bei der Analyse: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()