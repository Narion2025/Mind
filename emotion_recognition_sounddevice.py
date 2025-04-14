import websocket
import sounddevice as sd
import numpy as np
import json
import time
from datetime import datetime
import threading

# --- CONFIG ---
HUME_API_KEY = "YOUR_HUME_API_KEY"
HUME_WS_URL = "wss://api.hume.ai/v0/stream/models"
LOG_FILE = "emotion_log.txt"
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024

# --- Emotion Logging ---
def log_emotion(data):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now(datetime.timezone.utc).isoformat()
        f.write(f"{timestamp} | {data}\n")
        print(f"[LOG] {timestamp}: {data}")

# --- WebSocket Handlers ---
def on_message(ws, message):
    try:
        parsed = json.loads(message)
        predictions = parsed.get("predictions", [])
        for p in predictions:
            emotions = p.get("models", {}).get("emotions", {}).get("grouped_predictions", [])
            if emotions:
                log_emotion(emotions[0])
    except Exception as e:
        print("[Error Parsing]:", e)

def on_error(ws, error):
    print("[WebSocket Error]:", error)

def on_close(ws, *_):
    print("[WebSocket Closed]")

def on_open(ws):
    print("[🎤] Microphone stream started.")
    
    def callback(indata, *_):
        # Uncomment and define 'status' if needed, or remove this block
        # if status:
        #     print(status)
        audio_bytes = indata.astype(np.int16).tobytes()
        ws.send(audio_bytes, opcode=websocket.ABNF.OPCODE_BINARY)

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=BLOCK_SIZE, dtype='int16', callback=callback)
    stream.start()

# --- Start Emotion Stream ---
def start_emotion_stream():
    headers = {
        "Authorization": f"Bearer {HUME_API_KEY}"
    }
    ws = websocket.WebSocketApp(
        HUME_WS_URL + "?models=emotions",
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    print("[🧠] Connecting to Hume AI...")
    ws.run_forever()

if __name__ == "__main__":
    start_emotion_stream()
