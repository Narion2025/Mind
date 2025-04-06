require('dotenv').config();
const { processGPTResponse } = require('./gptResponseHandler');
const express = require('express');
const axios = require('axios');
const fs = require('fs');
const app = express();
const { analyzeEmotion } = require('./emotions');

app.use(express.json());

const PORT = process.env.PORT || 3000;

// Optional: Simulierter Emotionstest
const emotionResult = await analyzeEmotion(fakeWavBuffer);
console.log('🎭 Emotionserkennung:', emotionResult);


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
