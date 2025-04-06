require('dotenv').config();
const { processGPTResponse } = require('./gptResponseHandler');
const express = require('express');
const axios = require('axios');
const fs = require('fs');
const app = express();

app.use(express.json());

const PORT = process.env.PORT || 3000;

app.post('/speak', async (req, res) => {
    const text = req.body.text;
    if (!text) {
        return res.status(400).json({ error: 'No text provided' });
    }

    try {
        const voiceId = process.env.VOICE_ID;
        const apiKey = process.env.ELEVENLABS_API_KEY;

        const response = await axios.post(
            `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
            {
                text: text,
                model_id: "eleven_monolingual_v1",
                voice_settings: {
                    stability: 0.4,
                    similarity_boost: 0.6
                }
            },
            {
                headers: {
                    "xi-api-key": apiKey,
                    "Content-Type": "application/json"
                },
                responseType: 'stream'
            }
        );

        const outputPath = `./narion_output.mp3`;
        const writer = fs.createWriteStream(outputPath);
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
});

app.listen(PORT, () => {
    console.log(`Narion Voice Agent is running on port ${PORT}`);
});
