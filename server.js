import express from "express";
import path from "path";
import { fileURLToPath } from "url";

// __dirname für ES Module herstellen
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Absolute Pfadangabe zum Public-Ordner
const publicPath = path.join(__dirname, "MIND-Dashboard-Bundle", "public");

const app = express();
const PORT = process.env.PORT || 8000;

// Static Assets bereitstellen
app.use(express.static(publicPath));

// Bei allen GETs: index.html zurückgeben
app.get("*", (_, res) => {
  res.sendFile(path.join(publicPath, "index.html"));
});

app.listen(PORT, () => {
  console.log(`🧠 Dashboard läuft auf http://localhost:${PORT}`);
});
