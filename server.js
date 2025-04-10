import 'dotenv/config';
import express from 'express';
import fs from 'fs';
import { analyzeEmotion } from './emotions.js';

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

(async () => {
    try {
        // Optional: Simulierter Emotionstest
        const fakeWavBuffer = Buffer.from([]); // Replace with actual buffer
        const emotionResult = await analyzeEmotion(fakeWavBuffer);
        console.log('🎭 Emotionserkennung:', emotionResult);

        const outputPath = `./narion_output.mp3`;
        const writer = fs.createWriteStream(outputPath);
        // Assuming `response.data` is defined elsewhere
        response.data.pipe(writer);

        writer.on('finish', () => {
            res.sendFile(outputPath, { root: __dirname });
        });

        writer.on('error', (err) => {
            console.error('Error writing file:', err);
            res.status(500).send('Failed to write audio file');
        });
    } catch (err) {
        console.error(err.response?.data || err.message);
        res.status(500).send('Error generating speech');
    }
})();

app.listen(PORT, () => {
    console.log(`Narion Voice Agent is running on port ${PORT}`);
});
