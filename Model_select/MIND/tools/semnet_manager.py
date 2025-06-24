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
    def __init__(self, semnet_path=None):
        """Initialize the semantic network manager.

        Parameters
        ----------
        semnet_path : str, optional
            Path to the semantic network directory. If not provided the path is
            resolved relative to this file so that the tools work even when
            executed from other directories.
        """

        if semnet_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            semnet_path = os.path.join(base_dir, "..", "semnet", "core")

        self.semnet_path = semnet_path
        self.graph = nx.Graph()
        self.load_network()

    def load_network(self):
        """Lädt das semantische Netzwerk"""
        concepts_file = os.path.join(self.semnet_path, "initial_concepts.json")

        if os.path.exists(concepts_file):
            with open(concepts_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Knoten hinzufügen
            for node_id, node_data in data["nodes"].items():
                self.graph.add_node(node_id, **node_data)

            # Kanten hinzufügen
            for rel_id, rel_data in data["relations"].items():
                self.graph.add_edge(
                    rel_data["from"],
                    rel_data["to"],
                    weight=rel_data["strength"],
                    type=rel_data["type"],
                )

    def add_concept(self, concept_id, label, concept_type="derived", connections=None):
        """Fügt neues Konzept hinzu"""
        node_data = {
            "label": label,
            "type": concept_type,
            "strength": 0.5,
            "connections": connections or [],
            "created": datetime.now().isoformat(),
            "last_activated": None,
            "evolution_score": 0.0,
        }

        self.graph.add_node(concept_id, **node_data)

        # Verbindungen erstellen
        for conn in connections or []:
            if conn in self.graph:
                self.graph.add_edge(concept_id, conn, weight=0.5, type="related")

        self.save_network()

    def strengthen_connection(self, node1, node2, increment=0.1):
        """Verstärkt Verbindung zwischen Konzepten"""
        if self.graph.has_edge(node1, node2):
            current_weight = self.graph[node1][node2]["weight"]
            new_weight = min(1.0, current_weight + increment)
            self.graph[node1][node2]["weight"] = new_weight
        else:
            self.graph.add_edge(node1, node2, weight=0.5, type="emerging")

        # Aktivierung updaten
        for node in [node1, node2]:
            self.graph.nodes[node]["last_activated"] = datetime.now().isoformat()

        self.save_network()

    def visualize_network(self, output_file="semnet_graph.png"):
        """Visualisiert das Netzwerk"""
        plt.figure(figsize=(12, 8))

        # Layout berechnen
        pos = nx.spring_layout(self.graph, k=2, iterations=50)

        # Knoten zeichnen
        node_colors = []
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get("type", "unknown")
            if node_type == "core_concept":
                node_colors.append("red")
            elif node_type == "process_concept":
                node_colors.append("blue")
            else:
                node_colors.append("green")

        nx.draw_networkx_nodes(
            self.graph, pos, node_color=node_colors, node_size=500, alpha=0.8
        )

        # Kanten zeichnen
        edge_weights = [self.graph[u][v]["weight"] for u, v in self.graph.edges()]
        nx.draw_networkx_edges(self.graph, pos, width=edge_weights, alpha=0.5)

        # Labels
        labels = {node: self.graph.nodes[node]["label"] for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=10)

        plt.title("MIND Semantic Network")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_file)
        print(f"✅ Netzwerk visualisiert: {output_file}")

    def save_network(self):
        """Speichert das Netzwerk"""
        # In nx Graph Format konvertieren
        data = {"nodes": {}, "relations": {}}

        for node in self.graph.nodes():
            data["nodes"][node] = self.graph.nodes[node]

        for i, (u, v) in enumerate(self.graph.edges()):
            data["relations"][f"rel_{i}"] = {
                "from": u,
                "to": v,
                "type": self.graph[u][v].get("type", "unknown"),
                "strength": self.graph[u][v].get("weight", 0.5),
            }

        # Speichern mit Backup
        concepts_file = os.path.join(self.semnet_path, "initial_concepts.json")
        backup_file = concepts_file + ".bak"

        if os.path.exists(concepts_file):
            os.rename(concepts_file, backup_file)

        with open(concepts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def analyze_network(self):
        """Analysiert Netzwerk-Eigenschaften"""
        analysis = {
            "nodes": len(self.graph.nodes()),
            "edges": len(self.graph.edges()),
            "density": nx.density(self.graph),
            "components": nx.number_connected_components(self.graph),
            "average_clustering": nx.average_clustering(self.graph),
            "central_nodes": [],
        }

        # Zentralität berechnen
        centrality = nx.betweenness_centrality(self.graph)
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]

        for node_id, score in top_central:
            analysis["central_nodes"].append(
                {
                    "id": node_id,
                    "label": self.graph.nodes[node_id]["label"],
                    "centrality": score,
                }
            )

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
        connections = sys.argv[4].split(",") if len(sys.argv) > 4 else []
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
        for node in analysis["central_nodes"]:
            print(f"  - {node['label']} (Zentralität: {node['centrality']:.3f})")
