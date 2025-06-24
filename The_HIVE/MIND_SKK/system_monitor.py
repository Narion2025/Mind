import yaml
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Konfiguration
base_dir = os.path.expanduser("~/Documents/GitHub/Mind/Narion_MIND_Cleaned_Structure")
skk_dir = os.path.join(base_dir, "skk")
system_dir = os.path.join(skk_dir, "system")
system_state_path = os.path.join(system_dir, "system_state.yaml")
strudel_registry_path = os.path.join(system_dir, "strudel_registry.yaml")
knoten_registry_path = os.path.join(system_dir, "knoten_registry.yaml")
kristall_registry_path = os.path.join(system_dir, "kristall_registry.yaml")
history_path = os.path.join(system_dir, "system_history.yaml")

def load_yaml(file_path):
    """Lädt eine YAML-Datei oder gibt ein leeres Dict zurück"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def save_yaml(file_path, data):
    """Speichert eine YAML-Datei"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def update_history():
    """Aktualisiert die Systemverlaufsdatei mit dem aktuellen Zustand"""
    system_state = load_yaml(system_state_path)
    history = load_yaml(history_path)
    
    # Heute als Schlüssel verwenden
    today = datetime.today().strftime("%Y-%m-%d")
    
    # Relevante Metriken für den Verlauf extrahieren
    history_entry = {
        "active_strudel_count": system_state.get('active_strudel_count', 0),
        "average_pull_factor": system_state.get('average_pull_factor', 0),
        "strudel_density": system_state.get('strudel_density', 'unbekannt'),
        "system_drift": system_state.get('system_drift', 'unbekannt'),
        "equilibrium_tension": system_state.get('equilibrium_tension', 0),
        "total_strudel": system_state.get('total_counters', {}).get('strudel', 0),
        "total_knoten": system_state.get('total_counters', {}).get('knoten', 0),
        "total_kristalle": system_state.get('total_counters', {}).get('kristalle', 0)
    }
    
    # In Verlauf einfügen
    history[today] = history_entry
    
    # Speichern
    save_yaml(history_path, history)
    print(f"📈 Systemverlauf aktualisiert für {today}")

def generate_report():
    """Generiert einen Textbericht zum aktuellen Systemzustand"""
    system_state = load_yaml(system_state_path)
    strudel_registry = load_yaml(strudel_registry_path)
    knoten_registry = load_yaml(knoten_registry_path)
    kristall_registry = load_yaml(kristall_registry_path)
    
    print("=== SKK-SYSTEMMONITOR BERICHT ===")
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    print("SYSTEMZUSTAND:")
    print(f"- Strudel: {system_state.get('active_strudel_count', 0)} aktiv von {system_state.get('total_counters', {}).get('strudel', 0)} total")
    print(f"- Knoten: {system_state.get('total_counters', {}).get('knoten', 0)} total")
    print(f"- Kristalle: {system_state.get('total_counters', {}).get('kristalle', 0)} total\n")
    
    print(f"Systemdrift: {system_state.get('system_drift', 'unbekannt')}")
    print(f"Strudeldichte: {system_state.get('strudel_density', 'unbekannt')}")
    print(f"Gleichgewichtsspannung: {system_state.get('equilibrium_tension', 0):.2f}")
    print(f"Durchschnittlicher Pull-Faktor: {system_state.get('average_pull_factor', 0):.2f}\n")
    
    print("KRITISCHE STRUDEL:")
    if system_state.get('critical_strudels', []):
        for strudel_id in system_state.get('critical_strudels', []):
            strudel_data = strudel_registry.get(strudel_id, {})
            print(f"- {strudel_id}: {strudel_data.get('name', 'Unbekannt')} (Pull: {strudel_data.get('current_pull_factor', 0):.2f})")
    else:
        print("- Keine kritischen Strudel aktiv")
    
    print(f"\nEMPFEHLUNG: {system_state.get('recommended_regulation', 'Keine Empfehlung')}")

def main():
    """Hauptfunktion für den Systemmonitor"""
    # Sicherstellen, dass Verzeichnisse existieren
    os.makedirs(system_dir, exist_ok=True)
    
    # Verlauf aktualisieren
    update_history()
    
    # Bericht generieren
    generate_report()

if __name__ == "__main__":
    main()