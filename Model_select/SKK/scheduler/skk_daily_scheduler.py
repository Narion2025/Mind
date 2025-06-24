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
