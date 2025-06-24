from marker_analyser import analyse


def test_analyse_basic():
    text = "focus on clarity and meta reflection once upon a time"
    result = analyse(text)
    assert result['coherence'] > 0
    assert result['meta'] > 0
    assert result['narrative_intent'] is True
