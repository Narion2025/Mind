import json
import os
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict

STORE_PATH = Path(os.getenv('SECRET_STORE') or Path(__file__).with_name('secrets.json'))

def _load() -> Dict[str, Dict]:
    if STORE_PATH.exists():
        return json.loads(STORE_PATH.read_text())
    return {}

def _save(data: Dict[str, Dict]) -> None:
    STORE_PATH.write_text(json.dumps(data))

def mask(val: str) -> str:
    if len(val) <= 8:
        return val[0] + '\u2022' * (len(val) - 1)
    return val[:3] + '\u2022\u2022\u2022\u2022' + val[-4:]

def set_secret(key: str, value: str) -> None:
    data = _load()
    data[key] = {
        'value': base64.b64encode(value.encode()).decode(),
        'updated_at': datetime.utcnow().isoformat()
    }
    _save(data)

def get_value(key: str) -> str | None:
    data = _load()
    if key in data:
        return base64.b64decode(data[key]['value']).decode()
    return None

def get_all() -> Dict[str, Dict]:
    return _load()

def delete_secret(key: str) -> None:
    data = _load()
    if key in data:
        del data[key]
        _save(data)
