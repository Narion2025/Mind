import glob
import os
from typing import List, Dict

import yaml
import toml


class MarkerGrapper:
    """Lädt Markerdateien und erkennt vorkommende Muster im Text."""

    def __init__(self, marker_dir: str = "config/markers", include_sets: List[str] | None = None,
                 filter_tags: List[str] | None = None):
        self.include_sets = set(include_sets or [])
        self.filter_tags = set(filter_tags or [])
        self.markers = []
        self._load_marker_files(marker_dir)

    def _load_marker_files(self, marker_dir: str):
        files = glob.glob(os.path.join(marker_dir, "*.yaml")) + glob.glob(os.path.join(marker_dir, "*.toml"))
        for path in files:
            data = None
            if path.endswith(".yaml"):
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            elif path.endswith(".toml"):
                data = toml.load(path)
            if not isinstance(data, dict):
                continue
            self._collect_markers(data)

    def _collect_markers(self, data: Dict):
        for name, spec in data.items():
            sets = set(spec.get("set") or spec.get("sets") or [])
            tags = set(spec.get("tags", []))
            patterns = spec.get("muster") or spec.get("patterns") or []
            if self.include_sets and not (self.include_sets & sets):
                continue
            if self.filter_tags and not (self.filter_tags & tags):
                continue
            self.markers.append({"name": name, "patterns": patterns, "tags": tags})

    def grap_text(self, text: str) -> List[str]:
        text_lower = text.lower()
        found = []
        for marker in self.markers:
            for p in marker["patterns"]:
                if p.lower() in text_lower:
                    found.append(marker["name"])
                    break
        return found
