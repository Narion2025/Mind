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

# Resolve base directory so the script works from any location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
            os.path.join(BASE_DIR, "..", "modules", "self"),
            os.path.join(BASE_DIR, "..", "modules", "core"),
            os.path.join(BASE_DIR, "..", "modules", "extensions"),
            os.path.join(BASE_DIR, "..", "semnet", "core"),
            os.path.join(BASE_DIR, "..", "semnet", "patches"),
            os.path.join(BASE_DIR, "..", "semnet", "registry"),
            os.path.join(BASE_DIR, "..", "thoughts", "daily"),
            os.path.join(BASE_DIR, "..", "thoughts", "important"),
            os.path.join(BASE_DIR, "..", "thoughts", "dreams"),
            os.path.join(BASE_DIR, "..", "wiki", "concepts"),
            os.path.join(BASE_DIR, "..", "wiki", "research"),
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

        if analysis["nodes"] < 4:
            self.issues.append("Semnet hat weniger als 4 Knoten")

        if analysis["density"] < 0.1:
            self.issues.append("Semnet-Dichte sehr niedrig")

        if analysis["components"] > 1:
            self.issues.append("Semnet ist nicht vollständig verbunden")

        print(
            f"📊 Semnet: {analysis['nodes']} Knoten, Dichte: {analysis['density']:.3f}"
        )

    def check_thoughts(self):
        """Prüft Thoughts-Aktivität"""
        recent_thoughts = self.thoughts.list_thoughts(days=7)

        if len(recent_thoughts) == 0:
            self.issues.append("Keine Gedanken in den letzten 7 Tagen")

        analysis = self.thoughts.analyze_patterns()

        print(f"💭 Thoughts: {len(recent_thoughts)} in letzten 7 Tagen")

    def check_identity(self):
        """Prüft Identity Core"""
        identity_file = os.path.join(
            BASE_DIR, "..", "modules", "self", "identity_core.json"
        )

        if not os.path.exists(identity_file):
            self.issues.append("Identity Core fehlt!")
        else:
            with open(identity_file, "r") as f:
                identity = json.load(f)

            if "name" not in identity:
                self.issues.append("Identity Core unvollständig")
            else:
                print(f"🆔 Identity: {identity['name']} - OK")

    def check_activity(self):
        """Prüft System-Aktivität"""
        # Prüfe letzte Änderungen
        last_changes = []

        for root, dirs, files in os.walk(".."):
            for file in files:
                if file.endswith((".json", ".yaml", ".md")):
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
        if semnet_analysis["nodes"] < 10:
            print("  - Füge neue Konzepte zum Semnet hinzu")

        if self.issues:
            print("  - Führe 'mind_repair.sh' aus für automatische Reparatur")


if __name__ == "__main__":
    checker = MINDHealthCheck()
    checker.check_all()
