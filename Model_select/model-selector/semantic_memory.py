import yaml
from typing import Dict
from pathlib import Path


class MemoryClient:
    def __init__(self, patterns: Dict[str, list]):
        self.patterns = patterns


def load_memory(config_path: str) -> 'MemoryClient':
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    return MemoryClient(data.get('patterns', {}))


def extract_semantic_profile(text: str, client: MemoryClient) -> Dict[str, float]:
    words = text.lower().split()
    total = len(words) if words else 1
    profile = {}
    for key, patterns in client.patterns.items():
        count = sum(word in patterns for word in words)
        profile[key] = count / total
    return profile
