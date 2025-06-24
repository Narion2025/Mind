# Server Installation and GPT API Integration

This guide outlines how to deploy the Narion CoSD framework on a server and connect the analysis results to a custom GPT model through an API.

## 1. Evaluate Marker Definitions

The precision of the marker descriptions can be seen in `updated_marker_definitions.txt` and `narion-cosd-framework/markers/skk_bedeutungsfelder.yaml`. Each marker type includes definitions, characteristic patterns and lifespans. Example lines:

```yaml
Flügel:
  definition: "Entstehende Bedeutungen im Zwischenraum - vor der Form"
  markers:
    - "ahnung"
    - "gefühl"
    - "spüre"
  lebensdauer: "15 minuten"
Strudel:
  definition: "Anziehung zu emergenten Bedeutungen"
  warnung_hyperfokus: 8
  lebensdauer: "2 stunden"
```

These granular descriptions allow the analyzer to detect subtle shifts in meaning.

## 2. Build and Install the Tool

1. **Clone the repository** on your server and switch into the directory.
2. **Run the master setup script** to install all components and Python dependencies:
   ```bash
   bash master_setup_script.sh
   ```
   The script creates the `narion-cosd-framework` folder with the analyzer, SKK and MIND systems as described in `final_improvements_summary.md`.
3. **Verify the environment** with the health check:
   ```bash
   python3 narion-cosd-framework/system_health.py
   ```

## 3. Connect to a Custom GPT via API

The repository does not include built‑in GPT integration, but you can forward the YAML output of `skk_analyzer_standalone.py` to your model. Below is a simple example using the OpenAI Python library:

```python
import yaml
import openai

openai.api_key = "YOUR_API_KEY"

def send_results_to_gpt(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    prompt = f"Current marker resonance:\n{yaml.dump(data)}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Analyze drift behavior."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
```

Call `send_results_to_gpt()` after each analysis run or schedule it via `skk_daily_scheduler.py`. The GPT response can then be logged for further processing.

## 4. Real‑Time Updates

For real‑time interaction, run the analyzer in a loop or scheduler and call the API whenever a new report is generated. Ensure rate limits for your GPT service are respected and handle missing dependencies as shown in the troubleshooting guide.

