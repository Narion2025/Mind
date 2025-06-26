import random

COLORS = ["rot", "türkis", "blau", "grün", "violett"]


def do_color_test():
    print("Farbtest - wähle eine Farbe: " + ", ".join(COLORS))
    choice = input("Deine Farbe: ").strip().lower()
    if choice not in COLORS:
        choice = random.choice(COLORS)
        print(f"Unbekannte Farbe, nehme zufällig: {choice}")
    return choice


_COLOR_MAP = {
    "türkis": ("resonance", "fraud"),
    "rot": ("tension", "calm"),
    "blau": ("clarity", "chaos"),
    "grün": ("growth", "decay"),
    "violett": ("vision", "doubt"),
}


def get_marker_sets_for(color):
    return _COLOR_MAP.get(color, ("default", "contrast"))
