
// human_ai_voice_server.js
import express from "express";
import WebSocket from "ws";
import { createServer } from "http";
import { Readable } from "stream";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const VOICE_IDS = {
  Narion: "ff95f4b7-45e2-43ee-914b-141e7fa0153d",
  Sam: "b201d214-914c-4d0a-b8e4-54adfc14a0dd",
  Eloise: "5bbc32c1-a1f6-44e8-bedb-9870f23619e2"
};

const HUME_API_KEY = process.env.HUME_API_KEY;
const HUME_WS_URL = "wss://api.hume.ai/v0/stream/audio";

// Handle voice requests with emotion
app.post("/speak", async (req, res) => {
  const { user, text, emotion = "neutral" } = req.body;
  const voiceId = VOICE_IDS[user];

  if (!voiceId || !text) {
    return res.status(400).json({ error: "Invalid user or missing text" });
  }

  const ws = new WebSocket(HUME_WS_URL, {
    headers: { Authorization: `Bearer ${HUME_API_KEY}` }
  });

  ws.on("open", () => {
    ws.send(JSON.stringify({
      models: { prosody: { prediction: emotion } },
      voice: { voice_id: voiceId },
      text
    }));
  });

  let audioBuffers = [];
  ws.on("message", (data) => {
    const parsed = JSON.parse(data);
    if (parsed.audio) {
      audioBuffers.push(Buffer.from(parsed.audio, 'base64'));
    }
  });

  ws.on("close", () => {
    const audioStream = Readable.from(audioBuffers);
    res.setHeader("Content-Type", "audio/wav");
    audioStream.pipe(res);
  });

  ws.on("error", (err) => {
    console.error("WebSocket error:", err);
    res.status(500).json({ error: "Voice stream failed" });
  });
});

const server = createServer(app);
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
  console.log(`🔊 Human.AI Voice Server live on http://localhost:${PORT}`);
});
