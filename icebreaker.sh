#!/bin/bash

echo "🚀 Starte Icebreaker: Narion MIND Server stabilisieren..."

# Schritt 1: Watchdog installieren (pm2) und Tunnelbereitstellung (localtunnel)
echo "📦 Installiere pm2 und localtunnel (falls nicht vorhanden)..."
npm install -g pm2 localtunnel

# Schritt 2: Server starten und überwachen
echo "🧠 Starte und überwache MIND Server..."
pm2 start server.js --name mindserver --watch

# Schritt 3: Tunnel starten und URL loggen
echo "🌐 Starte LocalTunnel auf Port 8000..."
npx localtunnel --port 8000 > icebreaker-tunnel.log &

# Schritt 4: Warte kurz und zeige aktive Tunnel-URL
sleep 5
echo "📄 Aktive Tunnel-URL:"
grep -o 'https://[a-zA-Z0-9.-]*.loca.lt' icebreaker-tunnel.log

echo "✅ Icebreaker läuft. MIND ist stabilisiert. Überwachung aktiv."
