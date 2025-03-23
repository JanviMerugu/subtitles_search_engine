import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chromadb")  # Adjust path if needed
collection = chroma_client.get_or_create_collection("subtitle_embeddings")

# Path to subtitle data (adjusted to point to your dataset folder)
SUBTITLE_FILE = "dataset/subtitles.json"  # Update the path if needed

# Function to clean subtitles (remove timestamps, unnecessary characters)
def clean_subtitle(text):
    return text.replace("\n", " ").strip()  # Simple cleaning for now

# Function to chunk large subtitles
def chunk_text(text, chunk_size=50, overlap=10):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def process_and_store_embeddings():
    if not os.path.exists(SUBTITLE_FILE):
        print(f"❌ Error: Subtitle file not found at {SUBTITLE_FILE}")
        return

    # Load subtitle data
    with open(SUBTITLE_FILE, "r", encoding="utf-8") as f:
        subtitle_data = json.load(f)  # Assuming subtitles are stored as a JSON list

    print(f"🔄 Processing {len(subtitle_data)} subtitle entries...")

    doc_embeddings = []
    doc_texts = []

    # Process each subtitle entry
    for i, subtitle in enumerate(subtitle_data):
        cleaned_text = clean_subtitle(subtitle['text'])  # Assuming 'text' is the field name
        chunks = chunk_text(cleaned_text)

        # Generate embeddings for each chunk
        for chunk in chunks:
            embedding = model.encode(chunk, normalize_embeddings=True)
            doc_embeddings.append(embedding)
            doc_texts.append(chunk)

    # Store embeddings in ChromaDB
    print("💾 Storing embeddings in ChromaDB...")
    collection.add(
        embeddings=doc_embeddings,
        documents=doc_texts
    )
    
    print("✅ Embeddings successfully stored!")

if __name__ == "__main__":
    process_and_store_embeddings()
