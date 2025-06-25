import json
import base64
import os
from pathlib import Path
from typing import Dict
from datetime import datetime

env_path = os.getenv('SECRET_STORE')
store_path = Path(env_path) if env_path else Path(__file__).resolve().with_name('secrets_store.json')

def _load() -> Dict[str, Dict]:
    if store_path.exists():
        return json.loads(store_path.read_text())
    return {}


def _save(data: Dict[str, Dict]) -> None:
    store_path.write_text(json.dumps(data))


def mask(val: str) -> str:
    if len(val) <= 8:
        return val[0] + '\u2022' * (len(val) - 1)
    return val[:3] + '\u2022\u2022\u2022\u2022' + val[-4:]


def set_secret(key: str, value: str) -> None:
    data = _load()
    enc = base64.b64encode(value.encode()).decode()
    data[key] = {'value': enc, 'updated_at': datetime.utcnow().isoformat()}
    _save(data)


def get_secrets() -> Dict[str, Dict]:
    return _load()


def delete_secret(key: str) -> None:
    data = _load()
    if key in data:
        del data[key]
        _save(data)


def get_value(key: str) -> str | None:
    data = _load()
    if key in data:
        return base64.b64decode(data[key]['value']).decode()
    return None
