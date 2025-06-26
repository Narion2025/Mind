from pathlib import Path
import yaml

BASE_DIR = Path('mind_root') / 'schwarm'
MINDS_DIR = BASE_DIR / 'minds'


def create_agent(name: str, farbe: str, fokus: str, beschreibung: str) -> Path:
    """Erzeugt Dateien und Verzeichnisse für einen neuen Agenten."""
    agent_dir = BASE_DIR / name
    for sub in ['wiki', 'sort', 'narrative', 'lineage']:
        (agent_dir / sub).mkdir(parents=True, exist_ok=True)
    MINDS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        'name': name,
        'farbe': farbe,
        'fokus': fokus,
        'beschreibung': beschreibung,
        'ordner': str(agent_dir),
        'elemente': ['wiki/', 'sort/', 'narrative/', 'lineage/'],
    }
    yaml_path = MINDS_DIR / f'{name}.yaml'
    with yaml_path.open('w', encoding='utf-8') as fh:
        yaml.safe_dump(data, fh, allow_unicode=True)
    script = agent_dir / f'activate_{name}.py'
    if not script.exists():
        script.write_text('def activate():\n    pass\n')
    return yaml_path
