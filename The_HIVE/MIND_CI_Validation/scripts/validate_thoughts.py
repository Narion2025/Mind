import yaml
import jsonschema
import os

SCHEMA_PATH = "schema/thought_entry.schema.yml"
THOUGHTS_DIR = "thoughts/entries"

with open(SCHEMA_PATH) as f:
    schema = yaml.safe_load(f)

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

            data = yaml.safe_load("".join(front_matter))
            try:
                jsonschema.validate(instance=data, schema=schema)
                print(f"✅ {filename} valid.")
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {filename} invalid: {e.message}")
