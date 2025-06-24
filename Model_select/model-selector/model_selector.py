import yaml
from typing import Dict, Any
from pathlib import Path

from semantic_memory import load_memory, extract_semantic_profile
from marker_analyser import analyse as analyse_markers


with open(Path(__file__).parent / 'config' / 'model_selector.yaml', 'r', encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)

MEMORY_CLIENT = load_memory(str(Path(__file__).parent / 'config' / 'semantic_tools.yaml'))


def _match_rule(rule: Dict[str, Any], profile: Dict[str, Any]) -> bool:
    cond = rule.get('when', {})
    markers = cond.get('markers', {})
    for key, requirement in markers.items():
        value = profile['marker_profile'].get(key, 0)
        if 'lt' in requirement and not value < requirement['lt']:
            return False
        if 'gte' in requirement and not value >= requirement['gte']:
            return False
    semantic = cond.get('semantic', {})
    for key, requirement in semantic.items():
        value = profile['semantic_profile'].get(key, 0)
        if 'lt' in requirement and not value < requirement['lt']:
            return False
        if 'gte' in requirement and not value >= requirement['gte']:
            return False
    if cond.get('narrative_intent') and not profile['marker_profile'].get('narrative_intent'):
        return False
    if cond.get('requires_broad_context') and not profile.get('requires_broad_context'):
        return False
    return True


def select_model(text: str, previous_profile: Dict[str, Any] | None = None, system_state: Dict[str, Any] | None = None) -> Dict[str, Any]:
    sem_profile = extract_semantic_profile(text, MEMORY_CLIENT)
    marker_profile = analyse_markers(text, directory=str(Path(__file__).parent / 'config' / 'markers'))
    profile = {'marker_profile': marker_profile, 'semantic_profile': sem_profile}
    if previous_profile:
        profile['previous_profile'] = previous_profile
    if system_state:
        profile['system_state'] = system_state

    chosen = None
    reason = ''
    for rule in CONFIG.get('mappings', []):
        if _match_rule(rule, profile):
            chosen = rule['model']
            reason = f"matched rule for {chosen}"
            break
    result = {
        'chosen_model': chosen,
        'reason': reason,
        'profile': profile,
        'switch': bool(chosen)
    }
    return result
