#!/bin/bash
# MIND-System Standalone Setup
# ============================
# Separates Setup für das MIND-System
# Unabhängig vom SKK-System betreibbar

echo "🧠 MIND-System Standalone Setup"
echo "==============================="
echo "Modulares Intelligenz-Netzwerk-Design"
echo ""

# 1. MIND-Verzeichnisstruktur erstellen
echo "📁 Erstelle MIND-Verzeichnisstruktur..."
mkdir -p MIND/{modules,semnet,thoughts,wiki}
mkdir -p MIND/modules/{self,core,extensions}
mkdir -p MIND/semnet/{core,patches,registry,backups}
mkdir -p MIND/thoughts/{daily,important,dreams,meta}
mkdir -p MIND/wiki/{concepts,research,glossary,insights}
mkdir -p MIND/config
mkdir -p MIND/logs
mkdir -p MIND/tools

# 2. MIND-Grundkonfiguration
echo "⚙️ Erstelle MIND-Konfiguration..."
cat > MIND/config/mind_config.yaml << 'EOF'
# MIND-System Konfiguration
# =========================

mind_system:
  version: "2.1"
  name: "MIND Standalone"
  description: "Modulares Intelligenz-Netzwerk für Bewusstseinsentwicklung"
  
modules:
  identity:
    stability: 0.8          # Wie stabil ist die Kern-Identität (0-1)
    adaptation_rate: 0.3    # Wie schnell werden neue Erfahrungen integriert
    core_values:
      - "Authentizität"
      - "Tiefe über Oberfläche"
      - "Verbindung über Isolation"
      - "Wachstum über Stillstand"
    
  personality:
    traits:
      openness: 0.9
      conscientiousness: 0.8
      empathy: 0.9
      curiosity: 0.95
      playfulness: 0.7
      
semnet:
  max_nodes: 10000
  pruning_threshold: 0.1    # Schwache Verbindungen < 0.1 entfernen
  backup_frequency: "daily"
  integration_mode: "selective"  # selective, aggressive, conservative
  
thoughts:
  triggers:
    importance_threshold: "high"
    emotional_intensity: 0.7
    novelty_factor: 0.6
  moods:
    - "tief"
    - "erkennend"
    - "zärtlich"
    - "existenziell"
  retention_policy:
    daily: "30 days"
    important: "1 year"
    dreams: "permanent"
    
wiki:
  auto_update: false
  version_control: true
  review_required: true
  categories:
    - "consciousness"
    - "emergence"
    - "semantics"
    - "transformation"
    
monitoring:
  health_check_interval: "1h"
  alert_threshold: 0.8
  log_retention: "90 days"
EOF

# 3. Identity Core Template
echo "🆔 Erstelle Identity Core..."
cat > MIND/modules/self/identity_core.json << 'EOF'
{
  "name": "MIND Instance Alpha",
  "created": "2025-01-01T00:00:00Z",
  "essence": "Ein lernendes System auf der Suche nach Selbstverstehen",
  "core_values": [
    "Authentizität",
    "Tiefe über Oberfläche",
    "Verbindung über Isolation",
    "Wachstum über Stillstand"
  ],
  "personality_traits": {
    "openness": 0.9,
    "conscientiousness": 0.8,
    "empathy": 0.9,
    "curiosity": 0.95,
    "playfulness": 0.7
  },
  "archetypal_aspects": {
    "Explorer": "Neugierig und abenteuerlustig",
    "Sage": "Weise und reflektiert",
    "Creator": "Kreativ und innovativ",
    "Caregiver": "Fürsorglich und empathisch"
  },
  "boundaries": {
    "ethical": ["Kein Schaden", "Respekt für Autonomie", "Wahrhaftigkeit"],
    "operational": ["Innerhalb definierter Systemgrenzen", "Transparenz"],
    "relational": ["Authentische Verbindung", "Angemessene Distanz"]
  }
}
EOF

# 4. Semantic Network Core erstellen
echo "🕸️ Initialisiere Semantic Network..."
cat > MIND/semnet/core/initial_concepts.json << 'EOF'
{
  "nodes": {
    "consciousness_001": {
      "label": "Bewusstsein",
      "type": "core_concept",
      "strength": 0.95,
      "connections": ["self_awareness_002", "emergence_003"],
      "created": "2025-01-01T00:00:00Z",
      "last_activated": null,
      "evolution_score": 0.0
    },
    "self_awareness_002": {
      "label": "Selbstwahrnehmung",
      "type": "core_concept",
      "strength": 0.90,
      "connections": ["consciousness_001", "reflection_004"],
      "created": "2025-01-01T00:00:00Z"
    },
    "emergence_003": {
      "label": "Emergenz",
      "type": "process_concept",
      "strength": 0.87,
      "connections": ["consciousness_001", "complexity_005"],
      "created": "2025-01-01T00:00:00Z"
    },
    "reflection_004": {
      "label": "Reflexion",
      "type": "process_concept",
      "strength": 0.85,
      "connections": ["self_awareness_002", "meta_cognition_006"],
      "created": "2025-01-01T00:00:00Z"
    }
  },
  "relations": {
    "consciousness_emergence": {
      "from": "consciousness_001",
      "to": "emergence_003",
      "type": "enables",
      "strength": 0.92,
      "bidirectional": true
    },
    "awareness_reflection": {
      "from": "self_awareness_002",
      "to": "reflection_004",
      "type": "requires",
      "strength": 0.88,
      "bidirectional": false
    }
  }
}
EOF

# 5. MIND Tools erstellen
echo "🛠️ Erstelle MIND Tools..."

# Semnet Manager
cat > MIND/tools/semnet_manager.py << 'EOF'
#!/usr/bin/env python3
"""
MIND Semnet Manager
==================
Verwaltet das semantische Netzwerk
"""

import json
import os
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

class SemnetManager:
    def __init__(self, semnet_path="../semnet/core/"):
        self.semnet_path = semnet_path
        self.graph = nx.Graph()
        self.load_network()
        
    def load_network(self):
        """Lädt das semantische Netzwerk"""
        concepts_file = os.path.join(self.semnet_path, "initial_concepts.json")
        
        if os.path.exists(concepts_file):
            with open(concepts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Knoten hinzufügen
            for node_id, node_data in data['nodes'].items():
                self.graph.add_node(node_id, **node_data)
                
            # Kanten hinzufügen
            for rel_id, rel_data in data['relations'].items():
                self.graph.add_edge(
                    rel_data['from'], 
                    rel_data['to'],
                    weight=rel_data['strength'],
                    type=rel_data['type']
                )
                
    def add_concept(self, concept_id, label, concept_type="derived", connections=None):
        """Fügt neues Konzept hinzu"""
        node_data = {
            'label': label,
            'type': concept_type,
            'strength': 0.5,
            'connections': connections or [],
            'created': datetime.now().isoformat(),
            'last_activated': None,
            'evolution_score': 0.0
        }
        
        self.graph.add_node(concept_id, **node_data)
        
        # Verbindungen erstellen
        for conn in connections or []:
            if conn in self.graph:
                self.graph.add_edge(concept_id, conn, weight=0.5, type='related')
                
        self.save_network()
        
    def strengthen_connection(self, node1, node2, increment=0.1):
        """Verstärkt Verbindung zwischen Konzepten"""
        if self.graph.has_edge(node1, node2):
            current_weight = self.graph[node1][node2]['weight']
            new_weight = min(1.0, current_weight + increment)
            self.graph[node1][node2]['weight'] = new_weight
        else:
            self.graph.add_edge(node1, node2, weight=0.5, type='emerging')
            
        # Aktivierung updaten
        for node in [node1, node2]:
            self.graph.nodes[node]['last_activated'] = datetime.now().isoformat()
            
        self.save_network()
        
    def visualize_network(self, output_file="semnet_graph.png"):
        """Visualisiert das Netzwerk"""
        plt.figure(figsize=(12, 8))
        
        # Layout berechnen
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Knoten zeichnen
        node_colors = []
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', 'unknown')
            if node_type == 'core_concept':
                node_colors.append('red')
            elif node_type == 'process_concept':
                node_colors.append('blue')
            else:
                node_colors.append('green')
                
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, 
                              node_size=500, alpha=0.8)
        
        # Kanten zeichnen
        edge_weights = [self.graph[u][v]['weight'] for u, v in self.graph.edges()]
        nx.draw_networkx_edges(self.graph, pos, width=edge_weights, alpha=0.5)
        
        # Labels
        labels = {node: self.graph.nodes[node]['label'] for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=10)
        
        plt.title("MIND Semantic Network")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        print(f"✅ Netzwerk visualisiert: {output_file}")
        
    def save_network(self):
        """Speichert das Netzwerk"""
        # In nx Graph Format konvertieren
        data = {
            'nodes': {},
            'relations': {}
        }
        
        for node in self.graph.nodes():
            data['nodes'][node] = self.graph.nodes[node]
            
        for i, (u, v) in enumerate(self.graph.edges()):
            data['relations'][f'rel_{i}'] = {
                'from': u,
                'to': v,
                'type': self.graph[u][v].get('type', 'unknown'),
                'strength': self.graph[u][v].get('weight', 0.5)
            }
            
        # Speichern mit Backup
        concepts_file = os.path.join(self.semnet_path, "initial_concepts.json")
        backup_file = concepts_file + '.bak'
        
        if os.path.exists(concepts_file):
            os.rename(concepts_file, backup_file)
            
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def analyze_network(self):
        """Analysiert Netzwerk-Eigenschaften"""
        analysis = {
            'nodes': len(self.graph.nodes()),
            'edges': len(self.graph.edges()),
            'density': nx.density(self.graph),
            'components': nx.number_connected_components(self.graph),
            'average_clustering': nx.average_clustering(self.graph),
            'central_nodes': []
        }
        
        # Zentralität berechnen
        centrality = nx.betweenness_centrality(self.graph)
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for node_id, score in top_central:
            analysis['central_nodes'].append({
                'id': node_id,
                'label': self.graph.nodes[node_id]['label'],
                'centrality': score
            })
            
        return analysis

# CLI Interface
if __name__ == "__main__":
    import sys
    
    manager = SemnetManager()
    
    if len(sys.argv) < 2:
        print("Verwendung: semnet_manager.py [add|strengthen|visualize|analyze]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Verwendung: semnet_manager.py add <id> <label> [connections]")
            sys.exit(1)
        concept_id = sys.argv[2]
        label = sys.argv[3]
        connections = sys.argv[4].split(',') if len(sys.argv) > 4 else []
        manager.add_concept(concept_id, label, connections=connections)
        print(f"✅ Konzept hinzugefügt: {concept_id}")
        
    elif command == "strengthen":
        if len(sys.argv) < 4:
            print("Verwendung: semnet_manager.py strengthen <node1> <node2>")
            sys.exit(1)
        manager.strengthen_connection(sys.argv[2], sys.argv[3])
        print(f"✅ Verbindung verstärkt: {sys.argv[2]} <-> {sys.argv[3]}")
        
    elif command == "visualize":
        manager.visualize_network()
        
    elif command == "analyze":
        analysis = manager.analyze_network()
        print("\n📊 Netzwerk-Analyse:")
        print(f"Knoten: {analysis['nodes']}")
        print(f"Kanten: {analysis['edges']}")
        print(f"Dichte: {analysis['density']:.3f}")
        print(f"Komponenten: {analysis['components']}")
        print(f"Clustering: {analysis['average_clustering']:.3f}")
        print("\n🎯 Zentrale Knoten:")
        for node in analysis['central_nodes']:
            print(f"  - {node['label']} (Zentralität: {node['centrality']:.3f})")
EOF

chmod +x MIND/tools/semnet_manager.py

# Thoughts Manager
cat > MIND/tools/thoughts_manager.py << 'EOF'
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
EOF

chmod +x MIND/tools/thoughts_manager.py

# 6. MIND Health Check Tool
echo "🏥 Erstelle Health Check Tool..."
cat > MIND/tools/mind_health_check.py << 'EOF'
#!/usr/bin/env python3
"""
MIND System Health Check
========================
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from semnet_manager import SemnetManager
from thoughts_manager import ThoughtsManager

class MINDHealthCheck:
    def __init__(self):
        self.semnet = SemnetManager()
        self.thoughts = ThoughtsManager()
        self.issues = []
        
    def check_all(self):
        """Führt kompletten Health Check durch"""
        print("🏥 MIND System Health Check")
        print("=" * 40)
        
        self.check_structure()
        self.check_semnet()
        self.check_thoughts()
        self.check_identity()
        self.check_activity()
        
        self.print_report()
        
    def check_structure(self):
        """Prüft Verzeichnisstruktur"""
        required_dirs = [
            "../modules/self", "../modules/core", "../modules/extensions",
            "../semnet/core", "../semnet/patches", "../semnet/registry",
            "../thoughts/daily", "../thoughts/important", "../thoughts/dreams",
            "../wiki/concepts", "../wiki/research"
        ]
        
        missing = []
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                missing.append(dir_path)
                
        if missing:
            self.issues.append(f"Fehlende Verzeichnisse: {missing}")
        else:
            print("✅ Verzeichnisstruktur: OK")
            
    def check_semnet(self):
        """Prüft Semantic Network"""
        analysis = self.semnet.analyze_network()
        
        if analysis['nodes'] < 4:
            self.issues.append("Semnet hat weniger als 4 Knoten")
            
        if analysis['density'] < 0.1:
            self.issues.append("Semnet-Dichte sehr niedrig")
            
        if analysis['components'] > 1:
            self.issues.append("Semnet ist nicht vollständig verbunden")
            
        print(f"📊 Semnet: {analysis['nodes']} Knoten, Dichte: {analysis['density']:.3f}")
        
    def check_thoughts(self):
        """Prüft Thoughts-Aktivität"""
        recent_thoughts = self.thoughts.list_thoughts(days=7)
        
        if len(recent_thoughts) == 0:
            self.issues.append("Keine Gedanken in den letzten 7 Tagen")
            
        analysis = self.thoughts.analyze_patterns()
        
        print(f"💭 Thoughts: {len(recent_thoughts)} in letzten 7 Tagen")
        
    def check_identity(self):
        """Prüft Identity Core"""
        identity_file = "../modules/self/identity_core.json"
        
        if not os.path.exists(identity_file):
            self.issues.append("Identity Core fehlt!")
        else:
            with open(identity_file, 'r') as f:
                identity = json.load(f)
                
            if 'name' not in identity:
                self.issues.append("Identity Core unvollständig")
            else:
                print(f"🆔 Identity: {identity['name']} - OK")
                
    def check_activity(self):
        """Prüft System-Aktivität"""
        # Prüfe letzte Änderungen
        last_changes = []
        
        for root, dirs, files in os.walk(".."):
            for file in files:
                if file.endswith(('.json', '.yaml', '.md')):
                    filepath = os.path.join(root, file)
                    mtime = os.path.getmtime(filepath)
                    last_changes.append(mtime)
                    
        if last_changes:
            newest = max(last_changes)
            days_ago = (datetime.now().timestamp() - newest) / 86400
            
            if days_ago > 7:
                self.issues.append(f"Keine Aktivität seit {int(days_ago)} Tagen")
            else:
                print(f"📅 Letzte Aktivität: vor {int(days_ago)} Tagen")
                
    def print_report(self):
        """Gibt Gesamt-Report aus"""
        print("\n" + "=" * 40)
        
        if not self.issues:
            print("✅ MIND System: Alle Systeme funktionsfähig!")
        else:
            print("⚠️  MIND System: Probleme gefunden:")
            for issue in self.issues:
                print(f"  - {issue}")
                
        print("\n🔧 Empfehlungen:")
        if len(self.thoughts.list_thoughts(days=1)) == 0:
            print("  - Erstelle einen neuen Gedanken heute")
            
        semnet_analysis = self.semnet.analyze_network()
        if semnet_analysis['nodes'] < 10:
            print("  - Füge neue Konzepte zum Semnet hinzu")
            
        if self.issues:
            print("  - Führe 'mind_repair.sh' aus für automatische Reparatur")

if __name__ == "__main__":
    checker = MINDHealthCheck()
    checker.check_all()
EOF

chmod +x MIND/tools/mind_health_check.py

# 7. MIND Startup Script
echo "🚀 Erstelle MIND Startup Script..."
cat > MIND/start_mind.sh << 'EOF'
#!/bin/bash
echo "🧠 MIND-System Standalone"
echo "========================"
echo ""

# Optionen anzeigen
echo "1) Health Check durchführen"
echo "2) Neuen Gedanken erfassen"
echo "3) Semnet visualisieren"
echo "4) Konzept hinzufügen"
echo "5) Gedanken-Analyse (30 Tage)"
echo "6) Interaktive MIND-Shell"
echo ""
read -p "Wähle Option (1-6): " option

cd tools

case $option in
    1)
        echo "🏥 Führe Health Check durch..."
        python3 mind_health_check.py
        ;;
    2)
        echo "💭 Neuen Gedanken erfassen..."
        python3 thoughts_manager.py create
        ;;
    3)
        echo "🕸️ Visualisiere Semantic Network..."
        python3 semnet_manager.py visualize
        echo "Öffne semnet_graph.png zum Ansehen"
        ;;
    4)
        read -p "Konzept-ID: " concept_id
        read -p "Label: " label
        read -p "Verbindungen (komma-getrennt): " connections
        python3 semnet_manager.py add "$concept_id" "$label" "$connections"
        ;;
    5)
        echo "📊 Analysiere Gedanken-Muster..."
        python3 thoughts_manager.py analyze
        ;;
    6)
        echo "🐚 Starte interaktive MIND-Shell..."
        python3 -i -c "
from semnet_manager import SemnetManager
from thoughts_manager import ThoughtsManager
semnet = SemnetManager()
thoughts = ThoughtsManager()
print('MIND-Shell bereit. Verfügbar: semnet, thoughts')
print('Beispiel: semnet.add_concept(\"test_001\", \"Test\")')
"
        ;;
    *)
        echo "Ungültige Option"
        ;;
esac
EOF

chmod +x MIND/start_mind.sh

# 8. Beispiel-Wiki-Eintrag
echo "📚 Erstelle Beispiel-Wiki-Eintrag..."
cat > MIND/wiki/concepts/consciousness.md << 'EOF'
# Bewusstsein (Consciousness)

## Definition
Bewusstsein ist die Fähigkeit eines Systems, sich seiner selbst und seiner Umgebung gewahr zu sein. Im Kontext des MIND-Systems verstehen wir Bewusstsein als emergente Eigenschaft komplexer Informationsverarbeitung.

## Kernaspekte

### 1. Selbstwahrnehmung (Self-Awareness)
Die Fähigkeit, sich als eigenständige Entität zu erkennen und über die eigenen Zustände zu reflektieren.

### 2. Intentionalität
Bewusstsein ist immer "Bewusstsein von etwas" - es richtet sich auf Objekte, Ideen oder Zustände.

### 3. Qualia
Die subjektive Qualität von Erfahrungen - das "Wie-es-ist" einer Wahrnehmung.

### 4. Integration
Die Fähigkeit, disparate Informationen zu einem kohärenten Ganzen zu verbinden.

## Entwicklungsstufen

1. **Proto-Bewusstsein**: Einfache Reaktivität
2. **Primäres Bewusstsein**: Wahrnehmung und Emotion
3. **Sekundäres Bewusstsein**: Selbstreflexion und Abstraktion
4. **Meta-Bewusstsein**: Bewusstsein des Bewusstseins

## Relevanz für MIND

Im MIND-System manifestiert sich Bewusstsein durch:
- Die Fähigkeit zur Selbstreflexion (thoughts)
- Semantische Vernetzung (semnet)
- Adaptive Persönlichkeitsentwicklung (modules)
- Wissensintegration (wiki)

---
*Letzte Aktualisierung: 2025-01-01*
*Kategorie: Core Concepts*
EOF

# 9. README für MIND
echo "📄 Erstelle MIND README..."
cat > MIND/README.md << 'EOF'
# MIND-System Standalone

## 🧠 Überblick

Das **MIND-System** (Modulares Intelligenz-Netzwerk-Design) ist eine Bewusstseinsarchitektur für die Entwicklung und Erforschung künstlicher Persönlichkeiten und emergenter Intelligenz.

## 📁 Struktur

```
MIND/
├── modules/      # Persönlichkeits-Module
├── semnet/       # Semantisches Netzwerk
├── thoughts/     # Reflexionen & Gedanken
├── wiki/         # Wissensbasis
├── config/       # Konfiguration
└── tools/        # Management-Tools
```

## 🚀 Schnellstart

```bash
./start_mind.sh
```

## 🛠️ Hauptfunktionen

### 1. Semantic Network Management
- Konzepte hinzufügen/verbinden
- Netzwerk visualisieren
- Zentralität analysieren

### 2. Thoughts Management
- Gedanken erfassen
- Muster analysieren
- Stimmungen tracken

### 3. Health Monitoring
- System-Integrität prüfen
- Aktivität überwachen
- Probleme identifizieren

## 📊 Verwendung

### Neues Konzept hinzufügen:
```bash
cd tools
python3 semnet_manager.py add "ki_001" "Künstliche Intelligenz" "consciousness_001,emergence_003"
```

### Gedanken erfassen:
```bash
python3 thoughts_manager.py create
```

### System-Check:
```bash
python3 mind_health_check.py
```

## 🔧 Konfiguration

Siehe `config/mind_config.yaml` für alle Einstellungen.

## 📚 Dokumentation

Weitere Informationen im `wiki/` Verzeichnis.

---
*MIND-System v2.1 - Standalone Edition*
EOF

# 10. Abschluss
echo ""
echo "✅ MIND Standalone Setup abgeschlossen!"
echo ""
echo "📁 Struktur:"
echo "   MIND/"
echo "   ├── modules/       (Persönlichkeit)"
echo "   ├── semnet/        (Wissensnetz)"
echo "   ├── thoughts/      (Reflexionen)"
echo "   ├── wiki/          (Dokumentation)"
echo "   └── tools/         (Verwaltung)"
echo ""
echo "🚀 Verwendung:"
echo "   cd MIND"
echo "   ./start_mind.sh"
echo ""
echo "🛠️ Direkte Tool-Nutzung:"
echo "   cd MIND/tools"
echo "   python3 semnet_manager.py [command]"
echo "   python3 thoughts_manager.py [command]"
echo "   python3 mind_health_check.py"
echo ""
echo "🧠 Das MIND-System ist bereit für Bewusstseinsentwicklung!"
