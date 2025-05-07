import os
import yaml
from datetime import datetime

# Konfiguration
base_dir = os.path.expanduser("~/Documents/GitHub/Mind/Narion_MIND_Cleaned_Structure")
skk_dir = os.path.join(base_dir, "skk")
system_dir = os.path.join(skk_dir, "system")

# Verzeichnisse für SKK-Typen
strudel_dir = os.path.join(skk_dir, "strudel")
knoten_dir = os.path.join(skk_dir, "knoten")
kristall_dir = os.path.join(skk_dir, "kristalle")

# System-Dateien
system_state_path = os.path.join(system_dir, "system_state.yaml")
strudel_registry_path = os.path.join(system_dir, "strudel_registry.yaml")
knoten_registry_path = os.path.join(system_dir, "knoten_registry.yaml")
kristall_registry_path = os.path.join(system_dir, "kristall_registry.yaml")
history_path = os.path.join(system_dir, "system_history.yaml")

def save_yaml(file_path, data):
    """Speichert eine YAML-Datei"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def setup_directories():
    """Erstellt die benötigten Verzeichnisse"""
    for dir_path in [skk_dir, strudel_dir, knoten_dir, kristall_dir, system_dir]:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Verzeichnis erstellt: {dir_path}")

def create_initial_system_state():
    """Erstellt eine initiale System-State-Datei"""
    system_state = {
        "last_updated": datetime.now().isoformat(),
        "active_strudel_count": 0,
        "total_counters": {
            "strudel": 0,
            "knoten": 0,
            "kristalle": 0
        },
        "average_pull_factor": 0.0,
        "strudel_density": "niedrig",
        "system_drift": "stabil",
        "equilibrium_tension": 0.5,
        "critical_strudels": [],
        "recommended_regulation": "System initialisiert, bereit für SKK-Analyse"
    }
    
    save_yaml(system_state_path, system_state)
    print(f"✓ Initiale System-State-Datei erstellt: {system_state_path}")

def create_initial_registries():
    """Erstellt initiale Registry-Dateien"""
    # Leere Registry-Dateien erstellen
    save_yaml(strudel_registry_path, {})
    save_yaml(knoten_registry_path, {})
    save_yaml(kristall_registry_path, {})
    save_yaml(history_path, {})
    
    print(f"✓ Initiale Registry-Dateien erstellt")

def create_example_files():
    """Erstellt Beispiel-Dateien für jeden SKK-Typ"""
    # Beispiel-Strudel
    strudel_example = {
        "uuid": "example-strudel-uuid",
        "created_at": datetime.now().isoformat(),
        "source": "Setup-Skript",
        "mind_dynamics": {
            "mind_type": "strudel",
            "registry_id": "strudel:beispiel_sehnsucht",
            "origin_trace": "Beispiel",
            "matched_pattern": "sehne mich"
        },
        "embedding_ready_text": "Ich sehne mich nach mehr Verbindung zu der Tiefe in mir selbst.",
        "topics": ["Beispiel", "Sehnsucht", "Verbindung"],
        "tags": ["SKK", "strudel", "example"],
        "skk_triplet": {
            "strudel": {
                "id": "strudel:beispiel_sehnsucht",
                "name": "Sehnsucht nach Tiefe",
                "pull_factor_initial": 0.65,
                "current_pull_factor": 0.65,
                "decay_rate_per_day": 0.015,
                "last_activation": datetime.today().strftime("%Y-%m-%d"),
                "explosive_potential": False
            }
        }
    }
    
    # Beispiel-Knoten
    knoten_example = {
        "uuid": "example-knoten-uuid",
        "created_at": datetime.now().isoformat(),
        "source": "Setup-Skript",
        "mind_dynamics": {
            "mind_type": "knoten",
            "registry_id": "knoten:beispiel_pflichtbewusstsein",
            "origin_trace": "Beispiel",
            "matched_pattern": "muss immer"
        },
        "embedding_ready_text": "Ich muss immer zuverlässig sein, sonst bin ich wertlos.",
        "topics": ["Beispiel", "Pflicht", "Zuverlässigkeit"],
        "tags": ["SKK", "knoten", "example"],
        "skk_triplet": {
            "knoten": {
                "id": "knoten:beispiel_pflichtbewusstsein",
                "name": "Zuverlässigkeitszwang",
                "density_value": 0.75,
                "origin_trace": "Beispiel",
                "systemic_effects": ["Druck", "Selbstabwertung bei Fehlern"]
            }
        }
    }
    
    # Beispiel-Kristall
    kristall_example = {
        "uuid": "example-kristall-uuid",
        "created_at": datetime.now().isoformat(),
        "source": "Setup-Skript",
        "mind_dynamics": {
            "mind_type": "kristall",
            "registry_id": "kristall:beispiel_selbstakzeptanz",
            "origin_trace": "Beispiel",
            "matched_pattern": "erkannt, dass"
        },
        "embedding_ready_text": "Ich habe erkannt, dass ich nicht perfekt sein muss, sondern authentisch.",
        "topics": ["Beispiel", "Selbstakzeptanz", "Authentizität"],
        "tags": ["SKK", "kristall", "example"],
        "skk_triplet": {
            "kristall": {
                "id": "kristall:beispiel_selbstakzeptanz",
                "content": "Ich muss nicht perfekt sein sondern authentisch",
                "emergence": {
                    "from_strudel": "strudel:beispiel_sehnsucht",
                    "from_knoten": "knoten:beispiel_pflichtbewusstsein"
                },
                "stabilität": 0.8,
                "lichttiefe": 0.9,
                "integration_level": 0.7
            }
        }
    }
    
    # Speichern der Beispiele
    today = datetime.today().strftime("%Y-%m-%d")
    save_yaml(os.path.join(strudel_dir, f"{today}-strudel-beispiel.yaml"), strudel_example)
    save_yaml(os.path.join(knoten_dir, f"{today}-knoten-beispiel.yaml"), knoten_example)
    save_yaml(os.path.join(kristall_dir, f"{today}-kristall-beispiel.yaml"), kristall_example)
    
    # Registrieren der Beispiele
    strudel_registry = {"strudel:beispiel_sehnsucht": {
        "name": "Sehnsucht nach Tiefe",
        "current_pull_factor": 0.65,
        "last_activation": today,
        "decay_rate_per_day": 0.015,
        "explosive_potential": False,
        "references": [f"{today}-strudel-beispiel.yaml"]
    }}
    
    knoten_registry = {"knoten:beispiel_pflichtbewusstsein": {
        "name": "Zuverlässigkeitszwang",
        "density_value": 0.75,
        "last_activation": today,
        "references": [f"{today}-knoten-beispiel.yaml"]
    }}
    
    kristall_registry = {"kristall:beispiel_selbstakzeptanz": {
        "content": "Ich muss nicht perfekt sein sondern authentisch",
        "stabilität": 0.8,
        "lichttiefe": 0.9,
        "integration_level": 0.7,
        "created_at": today,
        "references": [f"{today}-kristall-beispiel.yaml"]
    }}
    
    save_yaml(strudel_registry_path, strudel_registry)
    save_yaml(knoten_registry_path, knoten_registry)
    save_yaml(kristall_registry_path, kristall_registry)
    
    # System-State aktualisieren
    system_state = {
        "last_updated": datetime.now().isoformat(),
        "active_strudel_count": 1,
        "total_counters": {
            "strudel": 1,
            "knoten": 1,
            "kristalle": 1
        },
        "average_pull_factor": 0.65,
        "strudel_density": "niedrig",
        "system_drift": "stabil",
        "equilibrium_tension": 0.5,
        "critical_strudels": [],
        "recommended_regulation": "System initialisiert mit Beispieldaten"
    }
    
    save_yaml(system_state_path, system_state)
    
    print(f"✓ Beispiel-Dateien erstellt und in Registries eingetragen")

def create_chatlog_starter():
    """Erstellt eine initiale Chatlog-Datei, falls keine existiert"""
    chatlog_path = "narion_chatlog.txt"
    if not os.path.exists(chatlog_path):
        with open(chatlog_path, 'w', encoding='utf-8') as f:
            f.write("# Narion Chat Log\n\n")
            f.write("Beginn einer neuen Reise. Ich sehne mich nach mehr Einsicht und Klarheit.\n\n")
            f.write("Ich muss immer perfekt sein, sonst bin ich nicht gut genug. Das ist ein tiefer Knoten in mir.\n\n")
            f.write("Heute wurde mir klar, dass ich nicht perfekt sein muss, sondern nur mein Bestes geben. Das ist befreiend.\n")
        print(f"✓ Initiale Chatlog-Datei erstellt: {chatlog_path}")
    else:
        print(f"ℹ️ Chatlog existiert bereits: {chatlog_path}")

def main():
    """Hauptprogramm für das Setup"""
    print("=== SKK-SYSTEM SETUP BEGINNT ===")
    
    setup_directories()
    create_initial_system_state()
    create_initial_registries()
    create_example_files()
    create_chatlog_starter()
    
    print("\n=== SKK-SYSTEM SETUP ABGESCHLOSSEN ===")
    print("Führen Sie nun 'python skk_autoanalyse.py' aus, um den Chatlog zu analysieren.")
    print("Oder fügen Sie weitere Einträge zur 'narion_chatlog.txt' hinzu.")

if __name__ == "__main__":
    main()
