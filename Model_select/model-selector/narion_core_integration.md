Example integration with Narion Assistant core.

```python
from semantic_memory import load_memory, extract_semantic_profile
from marker_analyser import analyse as analyse_markers
from model_selector import select_model

memory = load_memory("config/semantic_tools.yaml")

def handle_input(text, previous_profile=None, system_state=None):
    sem_profile = extract_semantic_profile(text, memory)
    marker_profile = analyse_markers(text)
    combined_profile = {"marker_profile": marker_profile, "semantic_profile": sem_profile}
    choice = select_model(text, previous_profile, system_state)
    assistant.switch_model(choice["chosen_model"])
    return assistant.generate(text, model=choice["chosen_model"])
```
