import websocket
import threading
import pyaudio
import json
from datetime import datetime, timezone

# --- CONFIG ---
HUME_API_KEY = "YOUR_HUME_API_KEY"
HUME_WS_URL = "wss://api.hume.ai/v0/stream/models"
LOG_FILE = "emotion_log.txt"

# --- Audio Setup ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# --- Emotion Logging ---
def log_emotion(data):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.utcnow().isoformat()
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"[LOG] {timestamp}: {data}")

# --- WebSocket Handling ---
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

def on_close(ws, close_status_code, close_msg):
    print("[WebSocket Closed]")

def on_open(ws):
    def run():
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        try:
            while True:
                audio_chunk = stream.read(CHUNK)
                ws.send(audio_chunk, opcode=websocket.ABNF.OPCODE_BINARY)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()

    threading.Thread(target=run).start()

# --- Start WebSocket Connection ---
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

    print("[🧠] Connecting to Hume AI Emotion API...")
    ws.run_forever()

if __name__ == "__main__":
    start_emotion_stream()
