import openai
import requests
import time
import os
from playsound import playsound
from dotenv import load_dotenv

# --- LOAD API KEYS ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- VOICE ID MAP ---
VOICE_ID_MAP = {
    "default": os.getenv("VOICE_ID_DEFAULT"),
    "calmness": os.getenv("VOICE_ID_CALM"),
    "joy": os.getenv("VOICE_ID_JOY"),
    "frustration": os.getenv("VOICE_ID_FRUSTRATION")
}

# --- CONFIG ---
LOG_PATH = "emotion_log.txt"
MP3_PATH = "narion_output.mp3"

# --- Read last emotion ---
def read_last_emotion():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
            if not lines:
                return "default", 0
            last = lines[-1]
            if "|" in last:
                _, data = last.split("|", 1)
                emotion_data = eval(data.strip())
                return emotion_data.get("name", "default"), emotion_data.get("score", 0)
    except Exception as e:
        print("[Emotion Read Error]", e)
    return "default", 0

# --- Modulate GPT Prompt ---
def modulate_prompt(emotion, score):
    if emotion == "frustration" and score > 0.7:
        return "The user is frustrated. Respond gently, calmly, and with reassurance."
    elif emotion == "joy" and score > 0.6:
        return "The user is joyful. Match their enthusiasm and respond brightly."
    elif emotion == "calmness" and score > 0.6:
        return "The user is calm. Reflect a thoughtful and composed tone."
    else:
        return "Respond normally."

# --- Get GPT Response ---
def get_gpt_response(system_prompt, user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# --- ElevenLabs Speech ---
def speak_text(text, emotion="default"):
    voice_id = VOICE_ID_MAP.get(emotion, VOICE_ID_MAP["default"])
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.6}
    }
    print(f"[🔊] Speaking with voice '{voice_id}' ({emotion}):", text)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open(MP3_PATH, "wb") as f:
            f.write(response.content)
        playsound(MP3_PATH)
    else:
        print("[ElevenLabs Error]:", response.status_code, response.text)

# --- Agent Loop ---
def agent_loop():
    print("[🧠] Narion Emotion Agent running...")
    while True:
        emotion, score = read_last_emotion()
        prompt = modulate_prompt(emotion, score)
        user_input = input("\n💬 What do you want to ask Narion? → ")

        gpt_response = get_gpt_response(prompt, user_input)
        speak_text(gpt_response, emotion)
        time.sleep(2)

if __name__ == "__main__":
    agent_loop()

