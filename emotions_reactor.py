import json
import time

# Beispielhafte Emotionseingaben aus Hume
emotion_sample = {
    "frustration": 0.82,
    "calmness": 0.2,
    "joy": 0.1
}

# Reaktionslogik
def generate_narion_prompt(emotions):
    if emotions.get("frustration", 0) > 0.7:
        return "Sprich beruhigend. Sag etwas, das den Nutzer entspannt."
    elif emotions.get("joy", 0) > 0.6:
        return "Sei enthusiastisch und freundlich."
    elif emotions.get("calmness", 0) > 0.7:
        return "Sprich reflektiert, mit ruhigem Tonfall."
    else:
        return "Sprich neutral."

# Beispielanwendung
if __name__ == "__main__":
    while True:
        # (später: live aus Hume-Stream lesen)
        print("[🧠] Eingehende Emotionen:", emotion_sample)
        mod_prompt = generate_narion_prompt(emotion_sample)
        print("[🎤] Narions Verhaltens-Modulation:", mod_prompt)

        # (später: Übergabe an GPT Prompting System + ElevenLabs)
        time.sleep(5)
