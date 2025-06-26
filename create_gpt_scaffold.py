import argparse
from pathlib import Path
import json

SERVER_JS_TEMPLATE = """const express = require('express');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const app = express();

const ankerFilePath = path.join(__dirname, '{name}.yaml');

if (!fs.existsSync(ankerFilePath)) {{
  fs.writeFileSync(ankerFilePath, '# auto-generiert\n', 'utf8');
  console.log('\u2705 {name}.yaml wurde erzeugt.');
}}

app.get('/init/anchors/{name}.yaml', (req, res) => {{
  res.setHeader('Content-Type', 'application/yaml');
  fs.createReadStream(ankerFilePath).pipe(res);
}});

app.listen(PORT, () => {{
  console.log(`\u{1F680} {name} Server l\u00E4uft auf http://localhost:${{PORT}}`);
}});
"""

YAML_TEMPLATE = """{name}_assistant:
  name: "{name}"
  role: "Resonanzfeld und semantischer Seher"
  description: >
    {description}

endpoint:
  url: "http://localhost:4060/{name}/reflect"
  method: POST
  expected_input:
    - marker_stream: List[Marker]
    - drift_state: DriftAchse
    - optional_context: String
  response:
    - insight_vector: PromptVector
    - knot_prediction: Optional[KnotID]
    - semantic_commentary: Text

triggers:
  - condition: "marker_count >= 3 && drift_aktiv"
    action: "call /{name}/reflect"
  - condition: "user_role == 'coach' && system_feedback_needed"
    action: "call /{name}/reflect"

actions:
  - name: "reflect"
    description: >
      Verarbeitet Marker und Drift, generiert semantischen InsightVector, optional Diagramm oder Knotenvorhersage. Kommentiert mit Bedeutungsschicht.
  - name: "comment"
    description: >
      Liefert reine Text-Resonanz – keine Entscheidung, sondern Spiegel.

constraints:
  - max_tokens: 800
  - call_frequency: "once per turn or on semantic shift"
  - no_diagnosis: true
  - no_decision_making: true

integration_notes:
  - {name} ben\u00F6tigt kein permanentes Memory, arbeitet kontextuell.
  - Nur aktivieren, wenn Feedback-Schicht gew\u00FCnscht ist.
  - Diagrammausgabe optional – durch knot_logic_module visualisierbar.
"""


def main():
    parser = argparse.ArgumentParser(description="Generate scaffold for a new GPT agent")
    parser.add_argument("name", help="Name of the GPT agent")
    parser.add_argument("--description", default="", help="Kurzbeschreibung oder Archetyp")
    args = parser.parse_args()

    base = Path(args.name)
    base.mkdir(exist_ok=True)

    # server.js
    server_js = base / "server.js"
    if not server_js.exists():
        server_js.write_text(SERVER_JS_TEMPLATE.format(name=args.name))

    # package.json
    package_json = base / "package.json"
    if not package_json.exists():
        data = {
            "name": args.name.lower(),
            "version": "1.0.0",
            "description": f"YAML-Anker Server f\u00FCr {args.name}",
            "main": "server.js",
            "scripts": {"start": "node server.js"},
            "dependencies": {"express": "^4.18.4"}
        }
        package_json.write_text(json.dumps(data, indent=2))

    lock = base / "package-lock.json"
    if not lock.exists():
        lock.write_text("{}\n")

    yaml_path = base / f"{args.name}.yaml"
    if not yaml_path.exists():
        yaml_path.write_text(YAML_TEMPLATE.format(name=args.name, description=args.description or ""))

    print(f"\u2714 Scaffold f\u00FCr {args.name} angelegt unter {base}")


if __name__ == "__main__":
    main()
