# resonance_filter.py
# Erste Struktur zur Filterung und Interpretation von Resonanzmustern

def erkenne_resonanz(muster):
    if "tiefe_resonanz" in muster and "paradoxe_klarheit" in muster:
        return "hoch_vertrauenswürdig"
    elif "rhetorische_stabilität" in muster:
        return "möglicherweise_maskiert"
    else:
        return "neutral"

def analysiere_dialogverlauf(dialog):
    veränderung = any("bruch" in abschnitt for abschnitt in dialog)
    rückkehr = any("rückbezug" in abschnitt for abschnitt in dialog)
    if veränderung and rückkehr:
        return "authentisch_dynamisch"
    else:
        return "statisch_oder_künstlich"