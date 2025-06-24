#!/usr/bin/env python3
"""
Semantic Network Rebuild Tool
Mergt SKK-Outputs in das MIND/semnet System
"""

import os
import json
import yaml
from datetime import datetime
import glob

def rebuild_semnet():
    """Rebuilde das semantische Netzwerk"""
    
    # Patches aus SKK_OUT laden
    patch_files = glob.glob("SKK_OUT/**/*.yaml", recursive=True)
    
    merged_count = 0
    
    for patch_file in patch_files:
        try:
            with open(patch_file, 'r', encoding='utf-8') as f:
                patch_data = yaml.safe_load(f)
            
            # In semnet/core integrieren
            base_name = os.path.basename(patch_file).replace('.yaml', '.json')
            target_file = f"MIND/semnet/core/{base_name}"
            
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(patch_data, f, ensure_ascii=False, indent=2)
            
            merged_count += 1
            
            # Processed patch verschieben
            processed_dir = "SKK_OUT/processed"
            os.makedirs(processed_dir, exist_ok=True)
            os.rename(patch_file, f"{processed_dir}/{os.path.basename(patch_file)}")
            
        except Exception as e:
            print(f"❌ Fehler bei {patch_file}: {e}")
    
    # Registry aktualisieren
    registry_entry = {
        'timestamp': datetime.now().isoformat(),
        'merged_patches': merged_count,
        'status': 'success'
    }
    
    with open("MIND/semnet/registry/last_rebuild.json", 'w') as f:
        json.dump(registry_entry, f, indent=2)
    
    print(f"✅ semnet rebuild: {merged_count} patches merged")

if __name__ == "__main__":
    rebuild_semnet()
