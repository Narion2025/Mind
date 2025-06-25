#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import textwrap


def main():
    parser = argparse.ArgumentParser(description="Create scaffold for a new GPT agent")
    parser.add_argument("name", help="Name of the GPT/agent")
    args = parser.parse_args()

    base = Path(args.name)
    base.mkdir(exist_ok=True)

    server_js = f"""const express = require('express');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const app = express();

const yamlPath = path.join(__dirname, '{args.name}.yaml');

if (!fs.existsSync(yamlPath)) {{
  fs.writeFileSync(yamlPath, '# auto-generated anchor\n', 'utf8');
  console.log('✅ {args.name}.yaml wurde erzeugt.');
}}

app.get('/init/anchors/{args.name}.yaml', (req, res) => {{
  res.setHeader('Content-Type', 'application/yaml');
  fs.createReadStream(yamlPath).pipe(res);
}});

app.listen(PORT, () => {{
  console.log(`🚀 {args.name} Server läuft unter http://localhost:${{PORT}}`);
}});
"""
    (base / "server.js").write_text(server_js)

    package_json = {
        "name": f"{args.name}-server",
        "version": "1.0.0",
        "scripts": {"start": "node server.js"},
        "dependencies": {"express": "^4.18.4"}
    }
    (base / "package.json").write_text(json.dumps(package_json, indent=2))
    (base / "package-lock.json").write_text('{}\n')
    (base / "node_modules").mkdir(exist_ok=True)

    yaml_content = textwrap.dedent(f"""
    {args.name}_assistant:
      name: "{args.name}"
      role: "Resonanzfeld und semantischer Seher"
      description: >
        {args.name} ist ein Interface für semantische Tiefenanalyse, systemische Mustererkennung
        und techno-emotionale Rückkopplung. Er wird aktiviert bei Drift, Markerhäufung
        oder explizitem Aufruf zur Deutung.

      endpoint:
        url: "http://localhost:4060/dante/reflect"
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
          action: "call /{args.name}/reflect"
        - condition: "user_role == 'coach' && system_feedback_needed"
          action: "call /{args.name}/reflect"

      actions:
        - name: "reflect"
          description: >
            Verarbeitet Marker und Drift, generiert semantischen InsightVector, optional
            Diagramm oder Knotenvorhersage. Kommentiert mit Bedeutungsschicht.
        - name: "comment"
          description: >
            Liefert reine Text-Resonanz – keine Entscheidung, sondern Spiegel.

      constraints:
        - max_tokens: 800
        - call_frequency: "once per turn or on semantic shift"
        - no_diagnosis: true
        - no_decision_making: true

      integration_notes:
        - {args.name} benötigt kein permanentes Memory, arbeitet kontextuell.
        - Nur aktivieren, wenn Feedback-Schicht gewünscht ist.
        - Diagrammausgabe optional – durch knot_logic_module visualisierbar.
    """)

    (base / f"{args.name}.yaml").write_text(yaml_content)

    print(f"📁 created GPT scaffold in {base}")


if __name__ == "__main__":
    main()
