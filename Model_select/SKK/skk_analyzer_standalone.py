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
            "kristalle": [],
            "metamarker": [],
        }

    def load_config(self, config_path):
        """Lädt SKK-Konfiguration"""
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.chunk_size = self.config["performance"]["chunk_size"]

    def setup_logging(self):
        """Konfiguriert Logging"""
        logging.basicConfig(
            filename="logs/skk_analyzer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def analyze_file(self, filepath):
        """Analysiert eine einzelne Datei"""
        self.logger.info(f"Analysiere Datei: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
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
        self._detect_metamarker()

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
            chunk = " ".join(words[i : i + self.chunk_size])
            chunks.append(chunk)

        return chunks

    def _analyze_chunk(self, chunk, chunk_idx):
        """Analysiert einen Text-Chunk auf Flügel"""
        flügel_config = self.config["bedeutungsfelder"]["flügel"]

        for marker in flügel_config["markers"]:
            pattern = rf"\b{marker}\w*\b"
            matches = re.findall(pattern, chunk.lower())

            if matches:
                flügel = {
                    "id": f'flügel_{chunk_idx}_{datetime.now().strftime("%H%M%S%f")}',
                    "chunk": chunk_idx,
                    "timestamp": datetime.now().isoformat(),
                    "marker": marker,
                    "matches": matches,
                    "count": len(matches),
                    "context": chunk[:200],
                    "bedeutung": self._interpret_bedeutung(marker, chunk),
                }
                self.bedeutungsfelder["flügel"].append(flügel)
                self.logger.info(f"Flügel erkannt: {flügel['id']}")

    def _form_strudel(self):
        """Bildet Strudel aus Flügeln"""
        strudel_config = self.config["bedeutungsfelder"]["strudel"]

        # Gruppiere Flügel nach Chunks
        chunk_flügel = defaultdict(list)
        for flügel in self.bedeutungsfelder["flügel"]:
            chunk_flügel[flügel["chunk"]].append(flügel)

        # Bilde Strudel wo >= 2 Flügel
        for chunk_idx, flügel_list in chunk_flügel.items():
            if len(flügel_list) >= 2:
                anziehungskraft = sum(f["count"] for f in flügel_list)

                strudel = {
                    "id": f'strudel_{chunk_idx}_{datetime.now().strftime("%H%M%S")}',
                    "timestamp": datetime.now().isoformat(),
                    "chunk": chunk_idx,
                    "flügel_ids": [f["id"] for f in flügel_list],
                    "anziehungskraft": anziehungskraft,
                    "hyperfokus": anziehungskraft
                    >= strudel_config["hyperfokus_threshold"],
                    "bedeutungsfeld": self._merge_bedeutungen(flügel_list),
                }

                if strudel["hyperfokus"]:
                    strudel["warnung"] = (
                        "HYPERFOKUS: Strudel verschlingt andere Bedeutungen!"
                    )
                    self.logger.warning(f"Hyperfokus-Strudel: {strudel['id']}")

                self.bedeutungsfelder["strudel"].append(strudel)
                self.logger.info(f"Strudel gebildet: {strudel['id']}")

    def _crystallize_knoten(self):
        """Verfestigt Knoten aus Strudeln"""
        knoten_config = self.config["bedeutungsfelder"]["knoten"]

        for strudel in self.bedeutungsfelder["strudel"]:
            if strudel["anziehungskraft"] > 5:
                rigidity = min(strudel["anziehungskraft"] / 10, 1.0)

                knoten = {
                    "id": f'knoten_{datetime.now().strftime("%Y%m%d_%H%M%S%f")}',
                    "timestamp": datetime.now().isoformat(),
                    "strudel_id": strudel["id"],
                    "strukturfestigkeit": rigidity,
                    "bedeutungsanker": strudel["bedeutungsfeld"],
                    "flexibilität": 1.0 - rigidity,
                }

                if rigidity >= knoten_config["rigidity_warning"]:
                    knoten["warnung"] = (
                        "Zu starre Struktur - kann Perspektive einschränken!"
                    )
                    self.logger.warning(f"Rigider Knoten: {knoten['id']}")

                self.bedeutungsfelder["knoten"].append(knoten)
                self.logger.info(f"Knoten kristallisiert: {knoten['id']}")

    def _create_kristalle(self):
        """Erschafft Kristalle aus Knoten"""
        kristall_config = self.config["bedeutungsfelder"]["kristalle"]

        if len(self.bedeutungsfelder["knoten"]) >= 2:
            # Nimm die letzten 2-3 Knoten
            recent_knoten = self.bedeutungsfelder["knoten"][-3:]

            kristall = {
                "id": f'kristall_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                "timestamp": datetime.now().isoformat(),
                "knoten_ids": [k["id"] for k in recent_knoten],
                "aha_moment": self._generate_aha_moment(recent_knoten),
                "erkenntnis": self._integrate_erkenntnisse(recent_knoten),
                "klarheit": kristall_config["clarity_threshold"],
                "bedeutung": "Integration disparater Bedeutungsfelder",
            }

            self.bedeutungsfelder["kristalle"].append(kristall)
            self.logger.info(f"Kristall erschaffen: {kristall['id']}")

    def _interpret_bedeutung(self, marker, context):
        """Interpretiert Bedeutung basierend auf Marker und Kontext"""
        bedeutungen = {
            "ahnung": "Vorbewusste Wahrnehmung erwacht",
            "gefühl": "Emotionale Resonanz entsteht",
            "spüre": "Körperliche Intuition meldet sich",
            "entsteh": "Werdender Prozess nimmt Form an",
            "drang": "Innerer Impuls drängt zur Manifestation",
            "sehnsucht": "Transzendentes Verlangen nach Ganzheit",
        }
        return bedeutungen.get(marker, "Unbenannte Regung im Zwischenraum")

    def _merge_bedeutungen(self, flügel_list):
        """Verschmilzt Flügel-Bedeutungen"""
        bedeutungen = [f["bedeutung"] for f in flügel_list]
        return " | ".join(set(bedeutungen))

    def _generate_aha_moment(self, knoten):
        """Generiert Aha-Moment-Beschreibung"""
        if len(knoten) >= 2:
            return f"Die Verbindung zwischen {knoten[0]['bedeutungsanker'][:30]} und {knoten[1]['bedeutungsanker'][:30]} wird klar!"
        return "Ein neues Verständnismuster kristallisiert sich!"

    def _integrate_erkenntnisse(self, knoten):
        """Integriert Erkenntnisse aus Knoten"""
        all_bedeutungen = [k["bedeutungsanker"] for k in knoten]
        return f"Synthese von {len(knoten)} Bedeutungsebenen: " + " → ".join(
            all_bedeutungen[:2]
        )

    def _detect_metamarker(self):
        """Erkennt Resonanzcluster aus Flügeln und Strudeln"""
        cfg = self.config.get("metamarker", {})
        fluegel_min = cfg.get("fluegel_min", 2)
        strudel_min = cfg.get("strudel_min", 1)
        timeframe = timedelta(seconds=cfg.get("timeframe_sec", 60))

        events = []
        for f in self.bedeutungsfelder["flügel"]:
            events.append(("flügel", datetime.fromisoformat(f["timestamp"])))
        for s in self.bedeutungsfelder["strudel"]:
            events.append(("strudel", datetime.fromisoformat(s["timestamp"])))

        events.sort(key=lambda x: x[1])

        for i in range(len(events)):
            counts = {"flügel": 0, "strudel": 0}
            start_time = events[i][1]
            for j in range(i, len(events)):
                if events[j][1] - start_time <= timeframe:
                    counts[events[j][0]] += 1
                else:
                    break
            if counts["flügel"] >= fluegel_min and counts["strudel"] >= strudel_min:
                metamarker = {
                    "id": f'metamarker_{start_time.strftime("%Y%m%d_%H%M%S")}',
                    "timestamp_start": start_time.isoformat(),
                    "timestamp_end": events[j - 1][1].isoformat(),
                    "kombination": counts,
                    "beschreibung": "Resonanzcluster aus Flügeln und Strudeln",
                }
                self.bedeutungsfelder["metamarker"].append(metamarker)
                self.logger.info(f"Metamarker erkannt: {metamarker['id']}")
                break

    def _generate_report(self):
        """Generiert umfassenden Analysebericht"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "statistik": {
                "flügel": len(self.bedeutungsfelder["flügel"]),
                "strudel": len(self.bedeutungsfelder["strudel"]),
                "knoten": len(self.bedeutungsfelder["knoten"]),
                "kristalle": len(self.bedeutungsfelder["kristalle"]),
                "metamarker": len(self.bedeutungsfelder["metamarker"]),
            },
            "warnungen": {
                "hyperfokus_strudel": sum(
                    1 for s in self.bedeutungsfelder["strudel"] if s.get("hyperfokus")
                ),
                "rigide_knoten": sum(
                    1 for k in self.bedeutungsfelder["knoten"] if "warnung" in k
                ),
            },
            "bedeutungsfelder": self.bedeutungsfelder,
            "narrative": self._generate_narrative(),
        }
        return report

    def _generate_narrative(self):
        """Generiert narrative Zusammenfassung"""
        narrative = []

        narrative.append(
            f"SKK-Analyse vom {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        )

        if self.bedeutungsfelder["flügel"]:
            narrative.append(
                f"🕊️ {len(self.bedeutungsfelder['flügel'])} Flügel entstanden - "
            )
            narrative.append(
                "Ahnungen und Gefühle, die noch keine Form gefunden haben.\n\n"
            )

        if self.bedeutungsfelder["strudel"]:
            narrative.append(
                f"🌀 {len(self.bedeutungsfelder['strudel'])} Strudel gebildet - "
            )
            narrative.append("Bedeutungen verdichten sich zu Anziehungspunkten.\n")
            hyperfokus = sum(
                1 for s in self.bedeutungsfelder["strudel"] if s.get("hyperfokus")
            )
            if hyperfokus:
                narrative.append(
                    f"⚠️ WARNUNG: {hyperfokus} Hyperfokus-Strudel erkannt!\n\n"
                )

        if self.bedeutungsfelder["knoten"]:
            narrative.append(
                f"🔗 {len(self.bedeutungsfelder['knoten'])} Knoten verfestigt - "
            )
            narrative.append(
                "Strukturen geben Halt, können aber auch einschränken.\n\n"
            )

        if self.bedeutungsfelder["kristalle"]:
            narrative.append(
                f"💎 {len(self.bedeutungsfelder['kristalle'])} Kristalle erschaffen - "
            )
            narrative.append("Aha-Momente bringen Licht in vorher dunkle Bereiche!\n\n")

        if self.bedeutungsfelder["metamarker"]:
            narrative.append(
                f"✨ {len(self.bedeutungsfelder['metamarker'])} Metamarker erkannt - Resonanzcluster weisen auf intensive Bedeutungsbildung hin.\n\n"
            )

        return "".join(narrative)

    def _save_results(self, report):
        """Speichert Analyseergebnisse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Hauptbericht
        report_file = f"analysen/skk_report_{timestamp}.yaml"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        with open(report_file, "w", encoding="utf-8") as f:
            yaml.dump(report, f, allow_unicode=True)

        # Einzelne Bedeutungsfelder
        for typ, elemente in report["bedeutungsfelder"].items():
            for element in elemente:
                element_file = f"{typ}/{element['id']}.yaml"
                os.makedirs(os.path.dirname(element_file), exist_ok=True)

                with open(element_file, "w", encoding="utf-8") as f:
                    yaml.dump(element, f, allow_unicode=True)

        self.logger.info(f"Ergebnisse gespeichert: {report_file}")
        print(f"✅ SKK-Analyse abgeschlossen: {report_file}")

        return report_file


# CLI Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SKK Standalone Analyzer")
    parser.add_argument("input", help="Eingabedatei oder -verzeichnis")
    parser.add_argument(
        "--config", default="config/skk_config.yaml", help="Konfigurationsdatei"
    )
    parser.add_argument(
        "--batch", action="store_true", help="Batch-Verarbeitung für Verzeichnis"
    )

    args = parser.parse_args()

    # Wechsle ins SKK-Verzeichnis
    if os.path.basename(os.getcwd()) != "SKK":
        os.chdir("SKK")

    analyzer = SKKStandaloneAnalyzer(args.config)

    if args.batch and os.path.isdir(args.input):
        # Batch-Verarbeitung
        for filename in os.listdir(args.input):
            if filename.endswith((".txt", ".log")):
                filepath = os.path.join(args.input, filename)
                print(f"Analysiere: {filename}")
                analyzer.analyze_file(filepath)
    else:
        # Einzeldatei
        analyzer.analyze_file(args.input)
