import os
from collections import Counter
from typing import List

import yaml


class MarkerSelfwriter:
    """Erstellt neue Marker aus dem Gesprächsverlauf."""

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        self.history: List[str] = []

    def observe(self, text: str):
        self.history.append(text)

    def _collect_candidates(self) -> List[str]:
        counter = Counter()
        for line in self.history:
            for word in line.lower().split():
                counter[word.strip('.,!?:;')] += 1
        return [w for w, c in counter.items() if c >= 3]

    def write_markers(self):
        for word in self._collect_candidates():
            path = os.path.join(self.base_dir, f"{word}.yaml")
            if os.path.exists(path):
                continue
            data = {
                word: {
                    "beschreibung": f"Automatisch generierter Marker für '{word}'",
                    "muster": [word],
                    "tags": ["drift", "auto"],
                }
            }
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True)
