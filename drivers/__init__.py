from importlib import import_module
from pathlib import Path

__all__ = ['load_drivers', 'MODELS']

MODELS = []

def load_drivers():
    global MODELS
    MODELS = []
    here = Path(__file__).parent
    for file in here.glob('*.py'):
        if file.name == '__init__.py':
            continue
        mod = import_module(f'drivers.{file.stem}')
        name = getattr(mod, 'MODEL_NAME', file.stem)
        MODELS.append(name)
    return MODELS

load_drivers()
