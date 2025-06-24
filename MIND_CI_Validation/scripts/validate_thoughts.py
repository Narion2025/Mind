try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None
try:
    import jsonschema
except ModuleNotFoundError:  # pragma: no cover
    jsonschema = None
import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BASE / "MIND_CI_Validation" / "schema" / "thought_entry.schema.yml"
THOUGHTS_DIR = BASE / "thoughts" / "entries"

if yaml:
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    required = schema.get('required', [])
else:
    schema = {}
    required = [
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
        if yaml:
            data = yaml.safe_load(''.join(front_matter)) or {}
        else:
            data = {}
            for line in front_matter:
                if ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip()] = v.strip()
        if jsonschema:
            try:
                jsonschema.validate(instance=data, schema=schema)
                print(f"✅ {filename} valid.")
            except jsonschema.exceptions.ValidationError as e:
                invalid += 1
                print(f"❌ {filename} invalid: {e.message}")
        else:
            missing = [r for r in required if r not in data]
            if missing:
                invalid += 1
                print(f"❌ {filename} missing: {', '.join(missing)}")
            else:
                print(f"✅ {filename} valid.")

if invalid:
    raise SystemExit(f"{invalid} invalid thought files")
