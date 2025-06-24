const express = require('express');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3002;
const app = express();

const ankerFilePath = path.join(__dirname, 'zora.anker.yaml');

// Erzeuge Datei bei Bedarf
if (!fs.existsSync(ankerFilePath)) {
  fs.writeFileSync(ankerFilePath, '# auto-generiert\n', 'utf8');
  console.log('✅ zora.anker.yaml wurde erzeugt.');
}

app.get('/init/anchors/zora.anker.yaml', (req, res) => {
  res.setHeader('Content-Type', 'application/yaml');
  fs.createReadStream(ankerFilePath).pipe(res);
});

app.listen(PORT, () => {
  console.log(`🚀 Zora-Server läuft unter http://localhost:${PORT}`);
});
