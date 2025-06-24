#!/bin/bash
# Narion CoSD Framework - Master Starter

echo "🧠 Narion CoSD Framework"
echo "========================"
echo ""
echo "Was möchten Sie starten?"
echo ""
echo "1) Enhanced Drift Analyzer (Haupttool)"
echo "2) SKK Standalone Analyse"
echo "3) MIND System Management"
echo "4) Vollständiger System-Check"
echo "5) Dokumentation anzeigen"
echo ""
read -p "Wählen Sie (1-5): " choice

case $choice in
    1)
        echo "🔍 Starte Enhanced Drift Analyzer..."
        cd analyzer && python3 enhanced_drift_analyzer_v5.py
        ;;
    2)
        echo "🌀 Starte SKK-System..."
        cd SKK && ./start_skk.sh
        ;;
    3)
        echo "🧠 Starte MIND-System..."
        cd MIND && ./start_mind.sh
        ;;
    4)
        echo "🏥 Führe System-Check durch..."
        echo ""
        echo "=== Analyzer Check ==="
        [ -f analyzer/enhanced_drift_analyzer_v5.py ] && echo "✅ Analyzer installiert" || echo "❌ Analyzer fehlt"
        
        echo ""
        echo "=== SKK Check ==="
        [ -d SKK ] && echo "✅ SKK-System installiert" || echo "❌ SKK fehlt"
        [ -f SKK/skk_analyzer_standalone.py ] && echo "✅ SKK Analyzer vorhanden" || echo "❌ SKK Analyzer fehlt"
        
        echo ""
        echo "=== MIND Check ==="
        [ -d MIND ] && echo "✅ MIND-System installiert" || echo "❌ MIND fehlt"
        [ -f MIND/tools/mind_health_check.py ] && echo "✅ MIND Tools vorhanden" || echo "❌ MIND Tools fehlen"
        
        echo ""
        echo "=== Python Check ==="
        python3 -c "import matplotlib, numpy, yaml, networkx; print('✅ Alle Python-Pakete installiert')" 2>/dev/null || echo "❌ Python-Pakete fehlen"
        ;;
    5)
        echo "📚 Zeige Dokumentation..."
        if [ -f README.md ]; then
            less README.md
        else
            echo "README.md nicht gefunden. Erstelle..."
            cat > README.md << 'README_END'
# Narion CoSD Framework

## Überblick
Das Narion CoSD (Co-emergenter Semantikdrift) Framework ist ein fortschrittliches System zur Analyse semantischer Bewusstseinsdrifts in Texten.

## Komponenten
- **Enhanced Drift Analyzer**: Hauptanalysetool mit GUI
- **SKK-System**: Strudel-Knoten-Kristalle Bedeutungsfeldanalyse
- **MIND-System**: Modulares Intelligenz-Netzwerk-Design

## Verwendung
Starten Sie mit: ./start_narion.sh

Weitere Details in den jeweiligen Unterverzeichnissen.
README_END
            less README.md
        fi
        ;;
    *)
        echo "Ungültige Auswahl"
        ;;
esac
