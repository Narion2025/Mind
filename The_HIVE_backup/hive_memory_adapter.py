# hive_memory_adapter.py
# Verbindung von The Hive zu Pinecone Vektor-Gedächtnis (aktualisiert für Pinecone SDK v3)

import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# 1. Umgebungsvariablen laden
def load_env(env_path=".envALL.txt"):
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(".env geladen.")
    else:
        raise FileNotFoundError("Keine .envALL.txt gefunden")

# 2. Pinecone-Verbindung herstellen (neue Syntax)
def connect_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENV")
    pc = Pinecone(api_key=api_key)
    print("Pinecone verbunden mit:", environment)
    return pc

# 3. Index vorbereiten
def get_or_create_index(pc, index_name="hive-core", dimension=1536):
    existing = [i.name for i in pc.list_indexes()]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="gcp", region="starter")
        )
        print("→ Neuer Index erstellt:", index_name)
    else:
        print("→ Index gefunden:", index_name)
    return pc.Index(index_name)

# 4. Embedding erzeugen (via OpenAI)
def embed_text(text, model="text-embedding-3-small"):
    client = OpenAI()
    api_key = os.getenv("OPENAI_API_KEY")
    client.api_key = api_key
    return client.embeddings.create(model=model, input=text).data[0].embedding

# 5. Abfrage an Pinecone senden
def query_similar(index, text, top_k=3):
    vector = embed_text(text)
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return results

# Einstiegspunkt
if __name__ == "__main__":
    load_env()
    pc = connect_pinecone()
    index = get_or_create_index(pc)

    beispieltext = "Systemische Emergenz erzeugt neue Formen."
    print("→ Embedding & Abfrage zu:", beispieltext)
    ergebnis = query_similar(index, beispieltext)
    for match in ergebnis.matches:
        print(f"{match.score:.3f} → {match.metadata}")
