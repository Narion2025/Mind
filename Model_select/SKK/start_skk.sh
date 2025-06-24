#!/bin/bash
echo "🌀 SKK-System Standalone"
echo "======================="
echo ""

# Optionen anzeigen
echo "1) Einzelanalyse durchführen"
echo "2) Batch-Analyse (Verzeichnis)"
echo "3) Scheduler starten (Daemon)"
echo "4) Test-Analyse"
echo ""
read -p "Wähle Option (1-4): " option

case $option in
    1)
        read -p "Dateiname eingeben: " filename
        python3 skk_analyzer_standalone.py "$filename"
        ;;
    2)
        read -p "Verzeichnis eingeben: " directory
        python3 skk_analyzer_standalone.py --batch "$directory"
        ;;
    3)
        echo "Starte SKK Scheduler..."
        cd scheduler && python3 skk_daily_scheduler.py
        ;;
    4)
        echo "Führe Test-Analyse durch..."
        python3 skk_analyzer_standalone.py text_inputs/test_bedeutungsfeld.txt
        ;;
    *)
        echo "Ungültige Option"
        ;;
esac
