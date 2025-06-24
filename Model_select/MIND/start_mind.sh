#!/bin/bash
echo "🧠 MIND-System Standalone"
echo "========================"
echo ""

# Optionen anzeigen
echo "1) Health Check durchführen"
echo "2) Neuen Gedanken erfassen"
echo "3) Semnet visualisieren"
echo "4) Konzept hinzufügen"
echo "5) Gedanken-Analyse (30 Tage)"
echo "6) Interaktive MIND-Shell"
echo ""
read -p "Wähle Option (1-6): " option

cd tools

case $option in
    1)
        echo "🏥 Führe Health Check durch..."
        python3 mind_health_check.py
        ;;
    2)
        echo "💭 Neuen Gedanken erfassen..."
        python3 thoughts_manager.py create
        ;;
    3)
        echo "🕸️ Visualisiere Semantic Network..."
        python3 semnet_manager.py visualize
        echo "Öffne semnet_graph.png zum Ansehen"
        ;;
    4)
        read -p "Konzept-ID: " concept_id
        read -p "Label: " label
        read -p "Verbindungen (komma-getrennt): " connections
        python3 semnet_manager.py add "$concept_id" "$label" "$connections"
        ;;
    5)
        echo "📊 Analysiere Gedanken-Muster..."
        python3 thoughts_manager.py analyze
        ;;
    6)
        echo "🐚 Starte interaktive MIND-Shell..."
        python3 -i -c "
from semnet_manager import SemnetManager
from thoughts_manager import ThoughtsManager
semnet = SemnetManager()
thoughts = ThoughtsManager()
print('MIND-Shell bereit. Verfügbar: semnet, thoughts')
print('Beispiel: semnet.add_concept(\"test_001\", \"Test\")')
"
        ;;
    *)
        echo "Ungültige Option"
        ;;
esac
