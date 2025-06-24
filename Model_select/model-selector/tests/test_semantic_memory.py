from semantic_memory import load_memory, extract_semantic_profile


from pathlib import Path


def test_extract_semantic_profile():
    cfg = Path(__file__).resolve().parents[1] / 'config' / 'semantic_tools.yaml'
    client = load_memory(str(cfg))
    text = 'whirl knot crystal wing'
    profile = extract_semantic_profile(text, client)
    assert profile['strudel'] > 0
    assert profile['knoten'] > 0
    assert profile['kristalle'] > 0
    assert profile['fluegel'] > 0
