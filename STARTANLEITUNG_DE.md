# Schnellstart für Narion Mind

Diese Anleitung erklärt in einfachen Worten, wie du das System startest, das Dashboard öffnest und Agenten hinzufügst. Die Schritte funktionieren unter Linux oder macOS. Falls du Windows nutzt, benötigst du eine Bash-Umgebung (z.B. durch WSL oder Git Bash).

## 1. Voraussetzungen
- [Git](https://git-scm.com/) und [Python 3](https://www.python.org/) müssen installiert sein.
- Optional: Node.js, falls du die Sprachfunktionen verwenden möchtest.

## 2. Projekt herunterladen
```bash
git clone https://github.com/Narion2025/Mind.git
cd Mind
pip install -r requirements.txt
```
Diese Befehle laden den Quellcode herunter und installieren die nötigen Python‑Pakete.

## 3. Server starten
Starte das Gateway mit
```bash
./start_gateway.sh
```
Falls der Port 8000 schon belegt ist, kannst du einen anderen Port über die Umgebungsvariable `API_PORT` setzen:
```bash
API_PORT=9000 ./start_gateway.sh
```
Mit `./start_gateway.sh --tunnel` bekommst du zusätzlich einen öffentlichen Link (via Localtunnel), über den andere dein Dashboard erreichen können.

## 4. Dashboard öffnen
Öffne im Browser die Adresse
```
http://localhost:8000/dashboard
```
(ersetze die 8000 durch deinen gewählten Port). Hier siehst du eine Liste der verfügbaren Funktionen und die aktuell bekannten Agenten.

- Über das Suchfeld kannst du nach Funktionen filtern.
- Der farbige Punkt zeigt, ob eine Funktion läuft (grün), noch nicht gestartet wurde (grau) oder Umgebungsvariablen fehlen (orange).
- Mit dem ▶‑Button startest du eine Funktion. Über „Logs“ lassen sich die Ausgaben anzeigen.

## 5. Agenten hinzufügen
Um einen neuen Agenten anzulegen, rufe im selben Browserfenster
```
http://localhost:8000/custom_gpt_setup.html
```
auf. Dort trägst du eine eindeutige GPT‑ID ein und klickst auf „Ankerpunkt erstellen“. Der Server legt daraufhin eine sogenannte *Anchor*-Datei an. Diese beschreibt Identität und Berechtigungen des Agenten.

Der fertige Anchor erscheint anschließend im Dashboard unter „Aktive Agenten". Über die API `POST /agents/{id}/action` kannst du einen Agenten verbinden, pausieren oder wieder löschen. Ein Beispiel für das Verbinden zeigt das README in Zeile 65 ff.

## 6. HTML direkt öffnen (optional)
Falls du die HTML‑Dateien ohne Server betrachten möchtest, findest du sie im Ordner `public/`. Durch Doppelklick auf `index.html` öffnet sich eine reduzierte Variante des Dashboards, die allerdings keine Serverfunktionen ausführt.

Viel Erfolg beim Ausprobieren!
