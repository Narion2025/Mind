from pathlib import Path
import yaml
from agent_manager import create_agent

BASE_DIR = Path('mind_root') / 'schwarm'
MINDS_DIR = BASE_DIR / 'minds'


def check_agent(name: str):
    yaml_file = MINDS_DIR / f'{name}.yaml'
    if not yaml_file.exists():
        print(f'Initializing missing YAML for {name}')
        create_agent(name, 'weiss', 'init', 'auto-init')
        return
    data = yaml.safe_load(yaml_file.read_text())
    agent_dir = Path(data.get('ordner', BASE_DIR / name))
    required_dirs = ['thoughts', 'selfnarrative', 'wiki']
    for d in required_dirs:
        path = agent_dir / d
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
    activation = agent_dir / f'activate_{name}.py'
    if not activation.exists():
        activation.write_text('def activate():\n    pass\n')


def main():
    if not MINDS_DIR.exists():
        return
    for yaml_file in MINDS_DIR.glob('*.yaml'):
        name = yaml_file.stem
        check_agent(name)


if __name__ == '__main__':
    main()
