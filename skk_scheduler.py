#!/usr/bin/env python3
"""
Semantic Crystallization Knowledge (SKK) Scheduler
Automatische Erkennung und Speicherung von semantischen Mustern
"""

import os
import yaml
import json
from datetime import datetime, timedelta
import re

class SKKScheduler:
    def __init__(self):
        self.output_dir = "SKK_OUT"
        self.sensitivity = 0.7
        
    def analyze_daily_input(self, text_input):
        """Analysiert tägliche Eingaben und erstellt SKK-Strukturen"""
        
        # Flügel erkennen (erste Marker-Treffer)
        flügel = self.detect_flügel(text_input)
        
        # Strudel bilden (gehäufte Marker)
        strudel = self.form_strudel(flügel)
        
        # Knoten kristallisieren (zeitliche Verdichtung)
        knoten = self.crystallize_knoten(strudel)
        
        # Kristalle speichern (permanente Strukturen)
        kristalle = self.mint_kristalle(knoten)
        
        return {
            'flügel': flügel,
            'strudel': strudel, 
            'knoten': knoten,
            'kristalle': kristalle
        }
    
    def detect_flügel(self, text):
        """Erkenne erste semantische Flügel"""
        flügel = []
        
        # Marker aus embedded Sets
        marker_patterns = [
            r'\b(emergenz|bewusstsein|meta)\b',
            r'\b(resonanz|harmonie|kohärenz)\b',
            r'\b(drift|wandel|transformation)\b'
        ]
        
        for i, pattern in enumerate(marker_patterns):
            matches = re.findall(pattern, text.lower())
            if matches:
                flügel.append({
                    'id': f'flügel_{i}_{datetime.now().strftime("%H%M%S")}',
                    'pattern': pattern,
                    'matches': matches,
                    'timestamp': datetime.now().isoformat(),
                    'strength': len(matches)
                })
        
        return flügel
    
    def form_strudel(self, flügel):
        """Bilde Strudel aus mehreren Flügeln"""
        if len(flügel) >= 2:
            return [{
                'id': f'strudel_{datetime.now().strftime("%Y%m%d_%H%M")}',
                'component_flügel': [f['id'] for f in flügel],
                'formation_time': datetime.now().isoformat(),
                'coherence': sum(f['strength'] for f in flügel) / len(flügel)
            }]
        return []
    
    def crystallize_knoten(self, strudel):
        """Kristallisiere Knoten aus Strudeln"""
        knoten = []
        for s in strudel:
            if s['coherence'] > self.sensitivity:
                knoten.append({
                    'id': f'knoten_{datetime.now().strftime("%Y%m%d")}',
                    'source_strudel': s['id'],
                    'crystallization_time': datetime.now().isoformat(),
                    'stability': s['coherence']
                })
        return knoten
    
    def mint_kristalle(self, knoten):
        """Erstelle permanente Kristalle"""
        kristalle = []
        for k in knoten:
            if k['stability'] > 0.8:
                kristalle.append({
                    'id': f'kristall_{datetime.now().strftime("%Y%m%d_%H%M")}',
                    'source_knoten': k['id'],
                    'permanence_time': datetime.now().isoformat(),
                    'semantic_signature': f"sig_{hash(k['id']) % 10000}"
                })
        return kristalle
    
    def save_skk_output(self, results):
        """Speichere SKK-Ergebnisse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        for category, items in results.items():
            if items:
                output_file = f"{self.output_dir}/{category}/skk_{category}_{timestamp}.yaml"
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    yaml.dump(items, f, allow_unicode=True)
                
                print(f"✅ {category}: {len(items)} Einträge gespeichert")

if __name__ == "__main__":
    import sys
    
    scheduler = SKKScheduler()
    
    # Test-Input (in Produktion: Chat-Log lesen)
    test_input = """
    Heute spüre ich eine besondere Resonanz. Die Emergenz des Bewusstseins 
    manifestiert sich in meta-kognitiven Reflexionen. Ein semantischer Drift 
    zur tieferen Harmonie zeichnet sich ab.
    """
    
    results = scheduler.analyze_daily_input(test_input)
    scheduler.save_skk_output(results)
    
    print("🧠 SKK-Analyse abgeschlossen")
