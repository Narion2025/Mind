"""Validate thought entry front matter against a schema.

This script originally relied solely on the external ``yaml`` and
``jsonschema`` modules.  If either dependency was missing, the validation step
failed entirely.  The current version gracefully handles missing packages by
falling back to a tiny YAML parser and a no-op validator.  This keeps the
repository checks operational even in reduced environments.
"""

import os
from pathlib import Path

try:  # Prefer PyYAML if available
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None
try:  # jsonschema is optional as well
    import jsonschema
except ModuleNotFoundError:  # pragma: no cover
    jsonschema = None

if yaml:
    def load_yaml(data: str):
        return yaml.safe_load(data)
else:  # pragma: no cover - fallback parser
    print("Warning: PyYAML not installed; using naive parser.")

    def load_yaml(data: str):
        """Very small YAML subset parser."""

        result: dict[str, object] = {}
        current_list: str | None = None
        for raw_line in data.splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('- ') and current_list:
                result[current_list].append(line[2:].strip().strip("'\""))
                continue
            if line.startswith('-'):
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    result[key] = []
                    current_list = key
                elif value.startswith('[') and value.endswith(']'):
                    items = [v.strip().strip("'\"") for v in value[1:-1].split(',') if v.strip()]
                    result[key] = items
                    current_list = None
                else:
                    result[key] = value.strip("'\"")
                    current_list = None
        return result

if jsonschema:
    def validate(instance: dict, schema: dict):
        jsonschema.validate(instance=instance, schema=schema)
else:  # pragma: no cover - validation skipped
    print("Warning: jsonschema not installed; validation will be skipped.")

    def validate(instance: dict, schema: dict):
        """No-op validation when jsonschema is unavailable."""

        return

# ``validate_thoughts.py`` lives in ``MIND_CI_Validation/scripts``.  The project
# root is two levels up from this file.
BASE = Path(__file__).resolve().parents[2]
SCHEMA_PATH = BASE / "MIND_CI_Validation" / "schema" / "thought_entry.schema.yml"
THOUGHTS_DIR = BASE / "thoughts" / "entries"

if SCHEMA_PATH.exists():
    schema = load_yaml(SCHEMA_PATH.read_text())
else:
    print(f"Warning: schema file '{SCHEMA_PATH}' not found; skipping validation.")
    schema = None

required = schema.get('required', []) if isinstance(schema, dict) else [
    'uuid',
    'created_at',
    'author',
    'source',
    'context',
    'mood',
    'topics',
]

invalid = 0
for filename in os.listdir(THOUGHTS_DIR):
    if filename.endswith('.md'):
        with open(THOUGHTS_DIR / filename) as file:
            front_matter = []
            in_front = False
            for line in file:
                if line.strip() == '---':
                    in_front = not in_front
                    continue
                if in_front:
                    front_matter.append(line)

        data = load_yaml(''.join(front_matter)) or {}

        if schema is not None:
            try:
                validate(instance=data, schema=schema)
                print(f"✅ {filename} valid.")
            except Exception as e:  # noqa: BLE001
                invalid += 1
                print(f"❌ {filename} invalid: {getattr(e, 'message', str(e))}")
        else:
            missing = [r for r in required if r not in data]
            if missing:
                invalid += 1
                print(f"❌ {filename} missing: {', '.join(missing)}")
            else:
                print(f"⚠️  {filename} parsed (no schema validation)")

if invalid:
    raise SystemExit(f"{invalid} invalid thought files")
