import os
import yaml
from datetime import datetime

BASE_PATH = os.path.expanduser("~/Documents/GitHub/Mind/Narion_MIND_Cleaned_Structure")
SKK_PATH = os.path.join(BASE_PATH, "skk")
LAYER0_PATH = os.path.join(BASE_PATH, "layer0.yaml")

def scan_ids(folder):
    """Sammelt alle YAML-Dateien im Ordner und extrahiert IDs"""
    ids = []
    folder_path = os.path.join(SKK_PATH, folder)
    for fname in os.listdir(folder_path):
        if fname.endswith(".yaml"):
            id_part = fname.split("-", maxsplit=3)[-1].replace(".yaml", "")
            full_id = f"{folder[:-1]}-{id_part}"
            ids.append(full_id)
    return ids

def load_layer0():
    try:
        with open(LAYER0_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def save_layer0(data):
    with open(LAYER0_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def update_layer0_yaml():
    layer0 = load_layer0()

    layer0["last_updated"] = datetime.now().isoformat()
    layer0["aktive_strudel"] = sorted(set(scan_ids("strudel")))
    layer0["aktive_knoten"] = sorted(set(scan_ids("knoten")))
    layer0["aktive_kristalle"] = sorted(set(scan_ids("kristalle")))

    layer0["metadata"] = {
        "total_strudel": len(layer0["aktive_strudel"]),
        "total_knoten": len(layer0["aktive_knoten"]),
        "total_kristalle": len(layer0["aktive_kristalle"]),
        "total_urspruenge": 3,
        "system_drift": "↪ aus system_state.yaml beziehen",
        "version": 1.1
    }

    save_layer0(layer0)
    print("✅ layer0.yaml aktualisiert.")

if __name__ == "__main__":
    update_layer0_yaml()
