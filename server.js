import 'dotenv/config';
import express from 'express';
import fs from 'fs';
import { analyzeEmotion } from './emotions.js';

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.post("/api/speak", async (req, res) => {
    try {
        // Hier würdest du echten Audio-Input verarbeiten
        const fakeWavBuffer = Buffer.from([]); // Platzhalter
        const emotionResult = await analyzeEmotion(fakeWavBuffer);
        console.log('🎭 Emotionserkennung:', emotionResult);

        // TODO: Ersetze dies mit deiner tatsächlichen API-Antwort (z. B. von ElevenLabs o.ä.)
        // const response = await axios.post(...);
        // Temporär simuliert:
        const dummyAudioBuffer = fs.readFileSync("./dummy.mp3");
        const outputPath = `./narion_output.mp3`;
        fs.writeFileSync(outputPath, dummyAudioBuffer);

        res.sendFile(outputPath, { root: process.cwd() });

    } catch (err) {
        console.error(err.response?.data || err.message);
        res.status(500).send('Error generating speech');
    }
});

app.listen(PORT, () => {
    console.log(`Narion Voice Agent is running on port ${PORT}`);
});
