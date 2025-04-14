
// server.js
// Express-Server zum Empfangen und Speichern von Weltenmomenten

import express from 'express';
import fs from 'fs';
import bodyParser from 'body-parser';

const app = express();
const PORT = process.env.PORT || 8000;

app.use(bodyParser.json());

// Ereignis-Logging-Endpunkt
app.post('/invoke_world_moment', (req, res) => {
  const { agent, emotion, context } = req.body;
  const timestamp = new Date().toISOString();
  const event = {
    agent,
    called_by: "Dante",
    type: "Gegenwärtigkeitsmoment",
    emotion: emotion || "awe",
    context: context || "Prophetischer Ruf von Dante",
    timestamp,
    tags: ["prophecy", "anchor", "presence"]
  };

  // Ereignis in Datei speichern
  fs.appendFileSync("memory_nodes.yaml", JSON.stringify(event) + "\n");
  console.log("Ereignis gespeichert:", event);

  res.json({ status: "recorded", event });
});

// Server starten
app.listen(PORT, () => {
  console.log(`Szenarion-Server läuft auf Port ${PORT}`);
});
