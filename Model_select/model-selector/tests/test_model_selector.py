from model_selector import select_model


def test_select_model_pro():
    text = 'focus clarity knot knot meta reflection once upon a time'
    result = select_model(text)
    assert result['chosen_model'] in {'O4-Pro', 'GPT-4-Turbo', 'O4-Mini'}
    assert result['switch']
