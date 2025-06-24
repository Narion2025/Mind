import os
import yaml
from typing import Dict


def load_markers(directory: str) -> Dict[str, list]:
    markers = {}
    for fname in os.listdir(directory):
        if fname.endswith('.yaml'):
            with open(os.path.join(directory, fname), 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                for key, values in data.items():
                    markers.setdefault(key, []).extend(values)
    return markers


from pathlib import Path


def analyse(text: str, directory: str | None = None) -> Dict[str, float]:
    if directory is None:
        directory = Path(__file__).parent / 'config' / 'markers'
    else:
        directory = Path(directory)
    markers = load_markers(str(directory))
    words = text.lower().split()
    total = len(words) if words else 1
    scores = {}
    for key, lst in markers.items():
        count = sum(word in lst for word in words)
        scores[key] = count / total
    scores['narrative_intent'] = any(phrase in text.lower() for phrase in markers.get('narrative_intent', []))
    return scores
