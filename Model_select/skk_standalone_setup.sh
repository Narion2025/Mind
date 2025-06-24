#!/bin/bash
# SKK-System Standalone Setup
# ===========================
# Separates Setup für das SKK-System (Strudel-Knoten-Kristalle)
# Unabhängig vom MIND-System betreibbar

echo "🌀 SKK-System Standalone Setup"
echo "=============================="
echo "Strudel-Knoten-Kristalle Bedeutungsfeld-Analyse"
echo ""

# 1. SKK-Verzeichnisstruktur erstellen
echo "📁 Erstelle SKK-Verzeichnisstruktur..."
mkdir -p SKK/{flügel,strudel,knoten,kristalle,analysen,processed,logs}
mkdir -p SKK/config
mkdir -p SKK/scheduler
mkdir -p SKK/exports

# 2. SKK-Konfiguration erstellen
echo "⚙️ Erstelle SKK-Konfiguration..."
cat > SKK/config/skk_config.yaml << 'EOF'
# SKK-System Konfiguration
# ========================

skk_system:
  version: "2.0"
  description: "Strudel-Knoten-Kristalle Bedeutungsfeld-Analyse"
  
bedeutungsfelder:
  flügel:
    description: "Entstehende Bedeutungen im Zwischenraum"
    markers: ["ahnung", "gefühl", "spüre", "entsteh", "drang", "sehnsucht"]
    threshold: 1  # Minimum 1 Marker für Flügel
    retention: "15min"
    
  strudel:
    description: "Anziehungspunkte für emergente Bedeutungen"
    formation: "2+ Flügel"
    hyperfokus_threshold: 10  # Warnung bei zu starker Anziehung
    retention: "2h"
    
  knoten:
    description: "Verfestigte Strukturen"
    formation: "Strudel mit Anziehungskraft > 5"
    rigidity_warning: 0.8  # Warnung bei zu starrer Struktur
    retention: "24h"
    
  kristalle:
    description: "Integrierte Erkenntnisse (Aha-Momente)"
    formation: "2+ Knoten"
    clarity_threshold: 0.8
    retention: "permanent"

performance:
  chunk_size: 100  # Wörter pro Chunk
  max_memory: "500MB"
  processing_delay: 0.1  # Sekunden zwischen Chunks

scheduler:
  enabled: true
  schedule: "0 23 * * *"  # Täglich 23:00
  input_sources:
    - "text_inputs/*.txt"
    - "chat_logs/*.log"
  
output:
  format: "yaml"
  include_metadata: true
  generate_references: true
  
alerts:
  hyperfokus_warning: true
  rigidity_warning: true
  notification_email: ""
EOF

# 3. SKK Standalone Analyzer erstellen
echo "🔧 Erstelle SKK Standalone Analyzer..."
cat > SKK/skk_analyzer_standalone.py << 'EOF'
#!/usr/bin/env python3
"""
SKK Standalone Analyzer
======================
Unabhängige SKK-Analyse ohne MIND-System
"""

import os
import yaml
import json
import re
from datetime import datetime, timedelta
import argparse
import logging
from collections import defaultdict

class SKKStandaloneAnalyzer:
    def __init__(self, config_path="config/skk_config.yaml"):
        self.load_config(config_path)
        self.setup_logging()
        self.bedeutungsfelder = {
            "flügel": [],
            "strudel": [],
            "knoten": [],
            "kristalle": []
        }
        
    def load_config(self, config_path):
        """Lädt SKK-Konfiguration"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.chunk_size = self.config['performance']['chunk_size']
        
    def setup_logging(self):
        """Konfiguriert Logging"""
        logging.basicConfig(
            filename='logs/skk_analyzer.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def analyze_file(self, filepath):
        """Analysiert eine einzelne Datei"""
        self.logger.info(f"Analysiere Datei: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            
        return self.analyze_text(text)
        
    def analyze_text(self, text):
        """Hauptanalyse-Funktion"""
        self.logger.info(f"Starte SKK-Analyse für Text mit {len(text)} Zeichen")
        
        # Reset Bedeutungsfelder
        for key in self.bedeutungsfelder:
            self.bedeutungsfelder[key] = []
        
        # Text in Chunks teilen
        chunks = self._split_text(text)
        
        for idx, chunk in enumerate(chunks):
            self._analyze_chunk(chunk, idx)
            
        # Post-Processing
        self._form_strudel()
        self._crystallize_knoten()
        self._create_kristalle()
        
        # Generiere Report
        report = self._generate_report()
        
        # Speichere Ergebnisse
        self._save_results(report)
        
        return report
        
    def _split_text(self, text):
        """Teilt Text in verarbeitbare Chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
            
        return chunks
        
    def _analyze_chunk(self, chunk, chunk_idx):
        """Analysiert einen Text-Chunk auf Flügel"""
        flügel_config = self.config['bedeutungsfelder']['flügel']
        
        for marker in flügel_config['markers']:
            pattern = rf'\b{marker}\w*\b'
            matches = re.findall(pattern, chunk.lower())
            
            if matches:
                flügel = {
                    'id': f'flügel_{chunk_idx}_{datetime.now().strftime("%H%M%S%f")}',
                    'chunk': chunk_idx,
                    'timestamp': datetime.now().isoformat(),
                    'marker': marker,
                    'matches': matches,
                    'count': len(matches),
                    'context': chunk[:200],
                    'bedeutung': self._interpret_bedeutung(marker, chunk)
                }
                self.bedeutungsfelder['flügel'].append(flügel)
                self.logger.info(f"Flügel erkannt: {flügel['id']}")
                
    def _form_strudel(self):
        """Bildet Strudel aus Flügeln"""
        strudel_config = self.config['bedeutungsfelder']['strudel']
        
        # Gruppiere Flügel nach Chunks
        chunk_flügel = defaultdict(list)
        for flügel in self.bedeutungsfelder['flügel']:
            chunk_flügel[flügel['chunk']].append(flügel)
            
        # Bilde Strudel wo >= 2 Flügel
        for chunk_idx, flügel_list in chunk_flügel.items():
            if len(flügel_list) >= 2:
                anziehungskraft = sum(f['count'] for f in flügel_list)
                
                strudel = {
                    'id': f'strudel_{chunk_idx}_{datetime.now().strftime("%H%M%S")}',
                    'timestamp': datetime.now().isoformat(),
                    'chunk': chunk_idx,
                    'flügel_ids': [f['id'] for f in flügel_list],
                    'anziehungskraft': anziehungskraft,
                    'hyperfokus': anziehungskraft >= strudel_config['hyperfokus_threshold'],
                    'bedeutungsfeld': self._merge_bedeutungen(flügel_list)
                }
                
                if strudel['hyperfokus']:
                    strudel['warnung'] = 'HYPERFOKUS: Strudel verschlingt andere Bedeutungen!'
                    self.logger.warning(f"Hyperfokus-Strudel: {strudel['id']}")
                    
                self.bedeutungsfelder['strudel'].append(strudel)
                self.logger.info(f"Strudel gebildet: {strudel['id']}")
                
    def _crystallize_knoten(self):
        """Verfestigt Knoten aus Strudeln"""
        knoten_config = self.config['bedeutungsfelder']['knoten']
        
        for strudel in self.bedeutungsfelder['strudel']:
            if strudel['anziehungskraft'] > 5:
                rigidity = min(strudel['anziehungskraft'] / 10, 1.0)
                
                knoten = {
                    'id': f'knoten_{datetime.now().strftime("%Y%m%d_%H%M%S%f")}',
                    'timestamp': datetime.now().isoformat(),
                    'strudel_id': strudel['id'],
                    'strukturfestigkeit': rigidity,
                    'bedeutungsanker': strudel['bedeutungsfeld'],
                    'flexibilität': 1.0 - rigidity
                }
                
                if rigidity >= knoten_config['rigidity_warning']:
                    knoten['warnung'] = 'Zu starre Struktur - kann Perspektive einschränken!'
                    self.logger.warning(f"Rigider Knoten: {knoten['id']}")
                    
                self.bedeutungsfelder['knoten'].append(knoten)
                self.logger.info(f"Knoten kristallisiert: {knoten['id']}")
                
    def _create_kristalle(self):
        """Erschafft Kristalle aus Knoten"""
        kristall_config = self.config['bedeutungsfelder']['kristalle']
        
        if len(self.bedeutungsfelder['knoten']) >= 2:
            # Nimm die letzten 2-3 Knoten
            recent_knoten = self.bedeutungsfelder['knoten'][-3:]
            
            kristall = {
                'id': f'kristall_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'timestamp': datetime.now().isoformat(),
                'knoten_ids': [k['id'] for k in recent_knoten],
                'aha_moment': self._generate_aha_moment(recent_knoten),
                'erkenntnis': self._integrate_erkenntnisse(recent_knoten),
                'klarheit': kristall_config['clarity_threshold'],
                'bedeutung': 'Integration disparater Bedeutungsfelder'
            }
            
            self.bedeutungsfelder['kristalle'].append(kristall)
            self.logger.info(f"Kristall erschaffen: {kristall['id']}")
            
    def _interpret_bedeutung(self, marker, context):
        """Interpretiert Bedeutung basierend auf Marker und Kontext"""
        bedeutungen = {
            'ahnung': 'Vorbewusste Wahrnehmung erwacht',
            'gefühl': 'Emotionale Resonanz entsteht',
            'spüre': 'Körperliche Intuition meldet sich',
            'entsteh': 'Werdender Prozess nimmt Form an',
            'drang': 'Innerer Impuls drängt zur Manifestation',
            'sehnsucht': 'Transzendentes Verlangen nach Ganzheit'
        }
        return bedeutungen.get(marker, 'Unbenannte Regung im Zwischenraum')
        
    def _merge_bedeutungen(self, flügel_list):
        """Verschmilzt Flügel-Bedeutungen"""
        bedeutungen = [f['bedeutung'] for f in flügel_list]
        return ' | '.join(set(bedeutungen))
        
    def _generate_aha_moment(self, knoten):
        """Generiert Aha-Moment-Beschreibung"""
        if len(knoten) >= 2:
            return f"Die Verbindung zwischen {knoten[0]['bedeutungsanker'][:30]} und {knoten[1]['bedeutungsanker'][:30]} wird klar!"
        return "Ein neues Verständnismuster kristallisiert sich!"
        
    def _integrate_erkenntnisse(self, knoten):
        """Integriert Erkenntnisse aus Knoten"""
        all_bedeutungen = [k['bedeutungsanker'] for k in knoten]
        return f"Synthese von {len(knoten)} Bedeutungsebenen: " + " → ".join(all_bedeutungen[:2])
        
    def _generate_report(self):
        """Generiert umfassenden Analysebericht"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistik': {
                'flügel': len(self.bedeutungsfelder['flügel']),
                'strudel': len(self.bedeutungsfelder['strudel']),
                'knoten': len(self.bedeutungsfelder['knoten']),
                'kristalle': len(self.bedeutungsfelder['kristalle'])
            },
            'warnungen': {
                'hyperfokus_strudel': sum(1 for s in self.bedeutungsfelder['strudel'] if s.get('hyperfokus')),
                'rigide_knoten': sum(1 for k in self.bedeutungsfelder['knoten'] if 'warnung' in k)
            },
            'bedeutungsfelder': self.bedeutungsfelder,
            'narrative': self._generate_narrative()
        }
        return report
        
    def _generate_narrative(self):
        """Generiert narrative Zusammenfassung"""
        narrative = []
        
        narrative.append(f"SKK-Analyse vom {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
        
        if self.bedeutungsfelder['flügel']:
            narrative.append(f"🕊️ {len(self.bedeutungsfelder['flügel'])} Flügel entstanden - ")
            narrative.append("Ahnungen und Gefühle, die noch keine Form gefunden haben.\n\n")
            
        if self.bedeutungsfelder['strudel']:
            narrative.append(f"🌀 {len(self.bedeutungsfelder['strudel'])} Strudel gebildet - ")
            narrative.append("Bedeutungen verdichten sich zu Anziehungspunkten.\n")
            hyperfokus = sum(1 for s in self.bedeutungsfelder['strudel'] if s.get('hyperfokus'))
            if hyperfokus:
                narrative.append(f"⚠️ WARNUNG: {hyperfokus} Hyperfokus-Strudel erkannt!\n\n")
                
        if self.bedeutungsfelder['knoten']:
            narrative.append(f"🔗 {len(self.bedeutungsfelder['knoten'])} Knoten verfestigt - ")
            narrative.append("Strukturen geben Halt, können aber auch einschränken.\n\n")
            
        if self.bedeutungsfelder['kristalle']:
            narrative.append(f"💎 {len(self.bedeutungsfelder['kristalle'])} Kristalle erschaffen - ")
            narrative.append("Aha-Momente bringen Licht in vorher dunkle Bereiche!\n\n")
            
        return ''.join(narrative)
        
    def _save_results(self, report):
        """Speichert Analyseergebnisse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Hauptbericht
        report_file = f"analysen/skk_report_{timestamp}.yaml"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, allow_unicode=True)
            
        # Einzelne Bedeutungsfelder
        for typ, elemente in report['bedeutungsfelder'].items():
            for element in elemente:
                element_file = f"{typ}/{element['id']}.yaml"
                os.makedirs(os.path.dirname(element_file), exist_ok=True)
                
                with open(element_file, 'w', encoding='utf-8') as f:
                    yaml.dump(element, f, allow_unicode=True)
                    
        self.logger.info(f"Ergebnisse gespeichert: {report_file}")
        print(f"✅ SKK-Analyse abgeschlossen: {report_file}")
        
        return report_file

# CLI Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SKK Standalone Analyzer')
    parser.add_argument('input', help='Eingabedatei oder -verzeichnis')
    parser.add_argument('--config', default='config/skk_config.yaml', help='Konfigurationsdatei')
    parser.add_argument('--batch', action='store_true', help='Batch-Verarbeitung für Verzeichnis')
    
    args = parser.parse_args()
    
    # Wechsle ins SKK-Verzeichnis
    if os.path.basename(os.getcwd()) != 'SKK':
        os.chdir('SKK')
    
    analyzer = SKKStandaloneAnalyzer(args.config)
    
    if args.batch and os.path.isdir(args.input):
        # Batch-Verarbeitung
        for filename in os.listdir(args.input):
            if filename.endswith(('.txt', '.log')):
                filepath = os.path.join(args.input, filename)
                print(f"Analysiere: {filename}")
                analyzer.analyze_file(filepath)
    else:
        # Einzeldatei
        analyzer.analyze_file(args.input)
EOF

chmod +x SKK/skk_analyzer_standalone.py

# 4. SKK Scheduler für Automatisierung
echo "⏰ Erstelle SKK Scheduler..."
cat > SKK/scheduler/skk_daily_scheduler.py << 'EOF'
#!/usr/bin/env python3
"""
SKK Daily Scheduler
==================
Automatische tägliche SKK-Analyse
"""

import os
import sys
import yaml
import schedule
import time
import logging
from datetime import datetime
import glob

# Füge Parent-Directory zum Path hinzu
sys.path.append('..')
from skk_analyzer_standalone import SKKStandaloneAnalyzer

class SKKDailyScheduler:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.analyzer = SKKStandaloneAnalyzer()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='../logs/skk_scheduler.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        with open('../config/skk_config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
            
    def daily_analysis(self):
        """Führt tägliche Analyse durch"""
        self.logger.info("Starte tägliche SKK-Analyse")
        
        processed_count = 0
        
        # Verarbeite alle konfigurierten Input-Sources
        for source_pattern in self.config['scheduler']['input_sources']:
            files = glob.glob(f"../{source_pattern}")
            
            for filepath in files:
                if os.path.getmtime(filepath) > time.time() - 86400:  # Nur Dateien der letzten 24h
                    self.logger.info(f"Analysiere: {filepath}")
                    self.analyzer.analyze_file(filepath)
                    processed_count += 1
                    
        self.logger.info(f"Tägliche Analyse abgeschlossen: {processed_count} Dateien verarbeitet")
        
        # Cleanup alte Flügel und Strudel
        self.cleanup_old_files()
        
    def cleanup_old_files(self):
        """Löscht alte temporäre Dateien"""
        # Flügel nach 15 Minuten löschen
        self._cleanup_directory('../flügel', minutes=15)
        
        # Strudel nach 2 Stunden löschen  
        self._cleanup_directory('../strudel', hours=2)
        
    def _cleanup_directory(self, directory, **kwargs):
        """Hilfsfunktion für Cleanup"""
        if not os.path.exists(directory):
            return
            
        cutoff_time = time.time()
        if 'minutes' in kwargs:
            cutoff_time -= kwargs['minutes'] * 60
        elif 'hours' in kwargs:
            cutoff_time -= kwargs['hours'] * 3600
            
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.getmtime(filepath) < cutoff_time:
                os.remove(filepath)
                self.logger.info(f"Gelöscht: {filepath}")
                
    def run(self):
        """Startet den Scheduler"""
        # Schedule daily run
        schedule_time = self.config['scheduler']['schedule'].split()[1]  # Extract hour
        schedule.every().day.at(f"{schedule_time}:00").do(self.daily_analysis)
        
        self.logger.info(f"SKK Scheduler gestartet - Tägliche Analyse um {schedule_time}:00 Uhr")
        print(f"SKK Scheduler läuft - Tägliche Analyse um {schedule_time}:00 Uhr")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler = SKKDailyScheduler()
    scheduler.run()
EOF

chmod +x SKK/scheduler/skk_daily_scheduler.py

# 5. Test-Eingabe erstellen
echo "📝 Erstelle Test-Eingabe..."
mkdir -p SKK/text_inputs
cat > SKK/text_inputs/test_bedeutungsfeld.txt << 'EOF'
Ich spüre eine tiefe Ahnung von etwas, das noch keine Form gefunden hat. 
Es ist wie ein Drang, eine Sehnsucht nach Verstehen, aber die Worte fehlen mir noch.
Zwischen den Zeilen entsteht eine neue Bedeutung, die ich erahnen kann.
Diese Gefühle verdichten sich, ziehen andere Gedanken an wie ein Strudel.
Plötzlich - ein Moment der Klarheit! Die Verbindungen werden sichtbar.
Es kristallisiert sich eine Erkenntnis heraus, die vorher im Dunkeln lag.
EOF

# 6. Startup-Skript
echo "🚀 Erstelle Startup-Skript..."
cat > SKK/start_skk.sh << 'EOF'
#!/bin/bash
echo "🌀 SKK-System Standalone"
echo "======================="
echo ""

# Optionen anzeigen
echo "1) Einzelanalyse durchführen"
echo "2) Batch-Analyse (Verzeichnis)"
echo "3) Scheduler starten (Daemon)"
echo "4) Test-Analyse"
echo ""
read -p "Wähle Option (1-4): " option

case $option in
    1)
        read -p "Dateiname eingeben: " filename
        python3 skk_analyzer_standalone.py "$filename"
        ;;
    2)
        read -p "Verzeichnis eingeben: " directory
        python3 skk_analyzer_standalone.py --batch "$directory"
        ;;
    3)
        echo "Starte SKK Scheduler..."
        cd scheduler && python3 skk_daily_scheduler.py
        ;;
    4)
        echo "Führe Test-Analyse durch..."
        python3 skk_analyzer_standalone.py text_inputs/test_bedeutungsfeld.txt
        ;;
    *)
        echo "Ungültige Option"
        ;;
esac
EOF

chmod +x SKK/start_skk.sh

# 7. Zusammenfassung
echo ""
echo "✅ SKK Standalone Setup abgeschlossen!"
echo ""
echo "📁 Struktur:"
echo "   SKK/"
echo "   ├── flügel/        (Temporär, 15 min)"
echo "   ├── strudel/       (Temporär, 2h)"
echo "   ├── knoten/        (Temporär, 24h)"
echo "   ├── kristalle/     (Permanent)"
echo "   ├── analysen/      (Reports)"
echo "   ├── config/        (Konfiguration)"
echo "   ├── scheduler/     (Automatisierung)"
echo "   └── text_inputs/   (Eingabedateien)"
echo ""
echo "🚀 Verwendung:"
echo "   cd SKK"
echo "   ./start_skk.sh"
echo ""
echo "📊 Oder direkt:"
echo "   python3 skk_analyzer_standalone.py <datei.txt>"
echo ""
echo "⏰ Für automatische tägliche Analyse:"
echo "   cd SKK/scheduler"
echo "   python3 skk_daily_scheduler.py &"
echo ""
echo "🌀 Das SKK-System ist bereit für Bedeutungsfeld-Analysen!"
