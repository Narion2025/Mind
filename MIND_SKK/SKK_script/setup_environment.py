import subprocess
import sys
import os
from pathlib import Path

env_name = "mind_env"

# Schritt 1: Virtuelle Umgebung erstellen
print(f"📦 Erstelle virtuelle Umgebung: {env_name}")
subprocess.run([sys.executable, "-m", "venv", env_name], check=True)

# Schritt 2: Pfade definieren
pip_path = Path(env_name) / "bin" / "pip"
python_path = Path(env_name) / "bin" / "python"

# Schritt 3: Pip aktualisieren und Pakete installieren
print("⬆️ Aktualisiere pip...")
subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)

print("📥 Installiere Pakete aus requirements.txt...")
subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

# Schritt 4: spaCy-Modell herunterladen
print("🌍 Lade spaCy Modell: de_core_news_md")
subprocess.run([python_path, "-m", "spacy", "download", "de_core_news_md"], check=True)

print("\n✅ Setup abgeschlossen!")
print(f"Aktiviere die Umgebung mit: source {env_name}/bin/activate")
