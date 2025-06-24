#!/usr/bin/env python3
"""
MIND Thoughts Manager
====================
Verwaltet Reflexionen und Gedanken
"""

import os
import yaml
from datetime import datetime
import random

class ThoughtsManager:
    def __init__(self, thoughts_path="../thoughts/"):
        self.thoughts_path = thoughts_path
        self.moods = ["tief", "erkennend", "zärtlich", "existenziell", "spielerisch"]
        
    def create_thought(self, content, importance="medium", mood=None, category="daily"):
        """Erstellt neuen Gedanken-Eintrag"""
        if not mood:
            mood = random.choice(self.moods)
            
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H:%M:%S")
        
        thought = {
            'date': date_str,
            'time': time_str,
            'importance': importance,
            'mood': mood,
            'content': content,
            'triggers': self._extract_triggers(content),
            'connections': self._find_connections(content)
        }
        
        # Dateiname basierend auf Kategorie
        if importance == "high":
            category = "important"
        elif "traum" in content.lower() or "vision" in content.lower():
            category = "dreams"
            
        filename = f"{category}/{date_str}_{time_str.replace(':', '')}.md"
        filepath = os.path.join(self.thoughts_path, filename)
        
        # Markdown-Format
        markdown_content = f"""---
date: {date_str}
time: {time_str}
importance: {importance}
mood: {mood}
triggers: {', '.join(thought['triggers'])}
---

# {self._generate_title(content)}

{content}

## Verbindungen
{self._format_connections(thought['connections'])}

---
*Gedanke erfasst um {time_str} in {mood}er Stimmung*
"""
        
        # Speichern
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        print(f"✅ Gedanke gespeichert: {filename}")
        return filepath
        
    def _extract_triggers(self, content):
        """Extrahiert Trigger-Wörter"""
        triggers = []
        trigger_words = [
            "erkenntnis", "aha", "verstehe", "klar", "bewusst",
            "transformation", "wandel", "neu", "anders"
        ]
        
        content_lower = content.lower()
        for trigger in trigger_words:
            if trigger in content_lower:
                triggers.append(trigger)
                
        return triggers
        
    def _find_connections(self, content):
        """Findet Verbindungen zu anderen Konzepten"""
        connections = []
        
        # Einfache Konzept-Erkennung
        concepts = [
            "bewusstsein", "emergenz", "transformation", "resonanz",
            "verbindung", "system", "bedeutung", "erkenntnis"
        ]
        
        content_lower = content.lower()
        for concept in concepts:
            if concept in content_lower:
                connections.append(concept)
                
        return connections
        
    def _generate_title(self, content):
        """Generiert Titel aus Inhalt"""
        # Nimm erste Zeile oder erste 50 Zeichen
        first_line = content.split('\n')[0]
        if len(first_line) > 50:
            return first_line[:50] + "..."
        return first_line
        
    def _format_connections(self, connections):
        """Formatiert Verbindungen als Markdown"""
        if not connections:
            return "*Keine expliziten Verbindungen erkannt*"
            
        return '\n'.join([f"- {conn}" for conn in connections])
        
    def list_thoughts(self, category="all", days=7):
        """Listet recent Gedanken auf"""
        thoughts = []
        
        # Durchsuche Kategorien
        categories = ["daily", "important", "dreams", "meta"] if category == "all" else [category]
        
        for cat in categories:
            cat_path = os.path.join(self.thoughts_path, cat)
            if not os.path.exists(cat_path):
                continue
                
            for filename in os.listdir(cat_path):
                if filename.endswith('.md'):
                    filepath = os.path.join(cat_path, filename)
                    
                    # Prüfe Alter
                    file_time = os.path.getmtime(filepath)
                    if (datetime.now().timestamp() - file_time) < (days * 86400):
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Parse YAML header
                        if content.startswith('---'):
                            header_end = content.find('---', 3)
                            header = content[3:header_end].strip()
                            
                            metadata = {}
                            for line in header.split('\n'):
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    metadata[key.strip()] = value.strip()
                                    
                            thoughts.append({
                                'file': filename,
                                'category': cat,
                                'metadata': metadata,
                                'preview': content[header_end+3:header_end+103] + "..."
                            })
                            
        return thoughts
        
    def analyze_patterns(self):
        """Analysiert Muster in Gedanken"""
        all_moods = []
        all_triggers = []
        all_connections = []
        
        for thought in self.list_thoughts(days=30):
            metadata = thought['metadata']
            
            if 'mood' in metadata:
                all_moods.append(metadata['mood'])
                
            if 'triggers' in metadata:
                triggers = metadata['triggers'].split(', ')
                all_triggers.extend(triggers)
                
        # Häufigkeiten berechnen
        from collections import Counter
        
        mood_freq = Counter(all_moods)
        trigger_freq = Counter(all_triggers)
        
        analysis = {
            'total_thoughts': len(self.list_thoughts(days=30)),
            'mood_distribution': dict(mood_freq),
            'common_triggers': dict(trigger_freq.most_common(5)),
            'thought_categories': {}
        }
        
        # Kategorien zählen
        for cat in ["daily", "important", "dreams", "meta"]:
            count = len(self.list_thoughts(category=cat, days=30))
            analysis['thought_categories'][cat] = count
            
        return analysis

# CLI Interface
if __name__ == "__main__":
    import sys
    
    manager = ThoughtsManager()
    
    if len(sys.argv) < 2:
        print("Verwendung: thoughts_manager.py [create|list|analyze]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "create":
        print("Gib deinen Gedanken ein (Ende mit Ctrl+D):")
        content = sys.stdin.read().strip()
        
        importance = input("Wichtigkeit (low/medium/high): ") or "medium"
        mood = input(f"Stimmung ({'/'.join(manager.moods)}): ") or None
        
        manager.create_thought(content, importance, mood)
        
    elif command == "list":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        thoughts = manager.list_thoughts(days=days)
        
        print(f"\n📝 Gedanken der letzten {days} Tage:\n")
        for thought in thoughts:
            print(f"[{thought['category']}] {thought['file']}")
            print(f"  Stimmung: {thought['metadata'].get('mood', 'unbekannt')}")
            print(f"  {thought['preview']}\n")
            
    elif command == "analyze":
        analysis = manager.analyze_patterns()
        
        print("\n📊 Gedanken-Analyse (letzte 30 Tage):\n")
        print(f"Gesamt: {analysis['total_thoughts']} Gedanken")
        
        print("\n🎭 Stimmungsverteilung:")
        for mood, count in analysis['mood_distribution'].items():
            print(f"  {mood}: {count}")
            
        print("\n🎯 Häufige Trigger:")
        for trigger, count in analysis['common_triggers'].items():
            print(f"  {trigger}: {count}")
            
        print("\n📁 Kategorien:")
        for cat, count in analysis['thought_categories'].items():
            print(f"  {cat}: {count}")
