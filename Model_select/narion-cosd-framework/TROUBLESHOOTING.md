# Narion CoSD Framework - Troubleshooting

## Häufige Probleme und Lösungen

### 1. Tool hängt sich auf / Performance-Probleme

**Symptome**: 
- GUI reagiert nicht mehr
- Analyse dauert sehr lange
- Hohe CPU-Auslastung

**Lösungen**:
- Textlänge reduzieren (optimal: 1000-5000 Wörter)
- Chunk-Size in Konfiguration verkleinern
- Performance-Modus aktivieren:
  ```python
  # In enhanced_drift_analyzer_v5.py:
  performance_chunks = 50  # Statt 100
  ```

### 2. ImportError: No module named 'xyz'

**Lösung**:
```bash
pip3 install matplotlib numpy pyyaml networkx
# oder
pip3 install --user matplotlib numpy pyyaml networkx
```

### 3. tkinter nicht gefunden

**Linux**:
```bash
sudo apt-get install python3-tk
```

**macOS**:
```bash
brew install python-tk
```

### 4. SKK-Analyse findet keine Bedeutungsfelder

**Prüfen Sie**:
- Enthält der Text SKK-Marker? (ahnung, gefühl, spüre, etc.)
- Ist die Sensitivität richtig eingestellt?
- Mindestlänge des Textes (>500 Wörter empfohlen)

### 5. MIND-System Health Check schlägt fehl

**Schritte**:
1. `cd MIND/tools`
2. `python3 mind_health_check.py`
3. Folgen Sie den Empfehlungen im Output

### 6. Visualisierungen werden nicht angezeigt

**Mögliche Ursachen**:
- Matplotlib Backend-Problem
- X11 Forwarding (bei SSH)

**Lösung**:
```python
import matplotlib
matplotlib.use('Agg')  # Für headless
# oder
matplotlib.use('TkAgg')  # Für GUI
```

## Performance-Optimierung

### Für große Texte (>10.000 Wörter)

1. Batch-Modus verwenden:
   ```bash
   python3 skk_analyzer_standalone.py --batch large_texts/
   ```

2. Chunk-Size anpassen:
   ```yaml
   # In skk_config.yaml:
   performance:
     chunk_size: 50  # Kleiner = weniger Speicher
   ```

3. GUI-Updates reduzieren:
   ```python
   # Nur alle 10 Chunks updaten
   if i % 10 == 0:
       gui.update()
   ```

## Debug-Modus

Für detaillierte Fehleranalyse:

```bash
# SKK Debug
cd SKK
python3 skk_analyzer_standalone.py --debug input.txt

# MIND Debug  
cd MIND/tools
python3 -m pdb mind_health_check.py

# Analyzer Debug
python3 -i enhanced_drift_analyzer_v5.py
# Dann in Python: import pdb; pdb.set_trace()
```

## Logs prüfen

```bash
# SKK Logs
tail -f SKK/logs/skk_analyzer.log

# MIND Logs
tail -f MIND/logs/mind_system.log

# System-Logs
journalctl -f | grep narion
```

## Kontakt

Bei weiteren Problemen:
- GitHub Issues: [repository-url]/issues
- E-Mail: support@narion-framework.ai
