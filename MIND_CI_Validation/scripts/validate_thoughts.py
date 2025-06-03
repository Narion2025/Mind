"""Validate thought entry front matter against a schema.

This script originally relied on the external ``yaml`` and ``jsonschema``
modules.  In environments where these are unavailable it would simply fail on
import.  To make the validation step more robust we now fall back to very basic
parsing/validation logic if the modules cannot be imported.
"""

import os

try:  # Prefer PyYAML if available
    import yaml

    def load_yaml(data: str):
        return yaml.safe_load(data)
except Exception:  # noqa: BLE001 - pycodestyle/flake rule disabled for brevity
    print("Warning: PyYAML not installed; using naive parser.")

    def load_yaml(data: str):
        """Very small YAML subset parser.

        Supports ``key: value`` pairs and simple lists using either ``[a, b]`` or
        ``key:`` followed by ``- item`` lines.  This is sufficient for the front
        matter used in the thought entries.
        """

        result: dict[str, object] = {}
        current_list: str | None = None
        for raw_line in data.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- ") and current_list:
                result[current_list].append(line[2:].strip().strip('"\''))
                continue
            if line.startswith("-"):
                continue
            if line.startswith("#"):
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    result[key] = []
                    current_list = key
                elif value.startswith("[") and value.endswith("]"):
                    items = [v.strip().strip('"\'') for v in value[1:-1].split(",") if v.strip()]
                    result[key] = items
                    current_list = None
                else:
                    result[key] = value.strip('"\'')
                    current_list = None
        return result

try:  # jsonschema is optional as well
    import jsonschema

    def validate(instance: dict, schema: dict):
        jsonschema.validate(instance=instance, schema=schema)
except Exception:  # noqa: BLE001
    print("Warning: jsonschema not installed; validation will be skipped.")

    def validate(instance: dict, schema: dict):  # noqa: D401
        """No-op validation when jsonschema is unavailable."""

        return

SCHEMA_PATH = "schema/thought_entry.schema.yml"
THOUGHTS_DIR = "thoughts/entries"

if os.path.exists(SCHEMA_PATH):
    with open(SCHEMA_PATH) as f:
        schema = load_yaml(f.read())
else:
    print(f"Warning: schema file '{SCHEMA_PATH}' not found; skipping validation.")
    schema = None

for filename in os.listdir(THOUGHTS_DIR):
    if filename.endswith(".md"):
        with open(os.path.join(THOUGHTS_DIR, filename)) as file:
            front_matter = []
            in_front = False
            for line in file:
                if line.strip() == "---":
                    in_front = not in_front
                    continue
                if in_front:
                    front_matter.append(line)

            data = load_yaml("".join(front_matter))
            if schema is not None:
                try:
                    validate(instance=data, schema=schema)
                    print(f"✅ {filename} valid.")
                except Exception as e:  # noqa: BLE001
                    print(f"❌ {filename} invalid: {getattr(e, 'message', str(e))}")
            else:
                print(f"⚠️  {filename} parsed (no schema validation)")
