import express from "express";
import path from "path";
import { fileURLToPath } from "url";

// __dirname für ES Module herstellen
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Absolute Pfadangabe zum Public-Ordner
// Die Dateien liegen im Ordner "mind_dashboard_bundle" im Repo
const publicPath = path.join(__dirname, "mind_dashboard_bundle");

const app = express();
const PORT = process.env.PORT || 8001;

// Static Assets bereitstellen
app.use(express.static(publicPath));

// Bei allen GETs: index.html zurückgeben
app.get("*", (_, res) => {
  res.sendFile(path.join(publicPath, "index.html"));
});
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🧠 Narion MIND Server läuft öffentlich auf Port ${PORT}`);
});
