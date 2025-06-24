import subprocess
import sys
import os
from pathlib import Path

env_name = "mind_env"

# Create virtual environment
print(f"📦 Creating virtual environment: {env_name}")
subprocess.run([sys.executable, "-m", "venv", env_name], check=True)

# Define pip path inside virtual environment
pip_path = Path(env_name) / "bin" / "pip"
python_path = Path(env_name) / "bin" / "python"

# Upgrade pip and install requirements
print("⬆️ Upgrading pip...")
subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)

print("📥 Installing packages from requirements.txt...")
subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

# Download spacy model
print("🌍 Downloading spaCy model: de_core_news_md")
subprocess.run([python_path, "-m", "spacy", "download", "de_core_news_md"], check=True)

print("\n✅ Setup complete! To activate, run:")
print(f"source {env_name}/bin/activate")
