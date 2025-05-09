#!/usr/bin/env python3
"""
imerion_bootstrap.py  ★  v3  (Pinecone SDK ≥ 3)

Erzeugt:
1. Pinecone‑Index  "imerion-core"
2. Drei Kern‑Embeddings (Wertschöpfung / Begegnung / Durchlässigkeit)
3. OpenAI‑Assistant  "Imerion"  mit Retrieval‑Tool auf diesen Index

Voraussetzungen:
  pip install -r requirements.txt   (openai≥1.13 , pinecone≥3 )
  .env mit  OPENAI_API_KEY / PINECONE_API_KEY / PINECONE_ENV  im selben Ordner
"""

# -----------------------------------------------------------------------------
# Imports & Keys
# -----------------------------------------------------------------------------
from pathlib import Path
import os, json
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone                # SDK v3 Einstiegspunkt

# -- .env laden ----------------------------------------------------------------
env_path = Path(__file__).resolve().parent / ".env"
if not env_path.is_file():
    raise FileNotFoundError(".env fehlt neben dem Script")
load_dotenv(env_path)

# -- OpenAI --------------------------------------------------------------------
client = OpenAI()
client.api_key = os.environ["OPENAI_API_KEY"]

# -- Pinecone‑Client -----------------------------------------------------------
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"],
              environment=os.environ["PINECONE_ENV"])

# -----------------------------------------------------------------------------
# Konfiguration
# -----------------------------------------------------------------------------
INDEX_NAME  = "imerion-core"
VECTOR_DIM  = 1536                     # text‑embedding‑3‑small
MODEL_EMBED = "text-embedding-3-small"
MODEL_CHAT  = "gpt-4.1-2025-04-14"    # ▶︎ Snapshot GPT‑4.1 (gewünscht)
SYSTEM_FILE = Path(__file__).parent / "systemprompt_imerion.txt"

# -----------------------------------------------------------------------------
# Texte → Embeddings
# -----------------------------------------------------------------------------
texts = {
    "wertschoepfung": (
        "Jede Handlung erzeugt Wert – oder raubt ihn. "
        "Wert ist keine Zahl, sondern Wirkung, die nicht rückgängig zu machen ist."
    ),
    "begegnung": (
        "Begegnung ist das zugelassene Überschreiten von Grenzen. "
        "Verletzliche Präsenz schafft das stabilste Netzwerk."
    ),
    "durchlaessigkeit": (
        "Durchlässigkeit ist Transparenz ohne Angst: Innen wird sichtbar, "
        "Außen wird integriert. Geheimnis löst sich zu Klarheit."
    ),
}

def embed(text: str) -> list[float]:
    return client.embeddings.create(model=MODEL_EMBED, input=text).data[0].embedding

print("→ Embeddings berechnen …")
vectors = {k: embed(t) for k, t in texts.items()}
print("   fertige Vektoren.")

# -----------------------------------------------------------------------------
# Pinecone‑Index (v3 Syntax)
# -----------------------------------------------------------------------------
if INDEX_NAME not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(name=INDEX_NAME, dimension=VECTOR_DIM, metric="cosine")
    print(f"→ Index '{INDEX_NAME}' erstellt.")
else:
    print(f"→ Index '{INDEX_NAME}' existiert bereits.")

index = pc.Index(INDEX_NAME)
index.upsert(vectors=[(f"imerion-{k}", v, {"label": k}) for k, v in vectors.items()])
print("→ 3 Kernvektoren hochgeladen.")

#