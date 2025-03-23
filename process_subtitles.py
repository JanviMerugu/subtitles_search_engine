import os
import chromadb
from sentence_transformers import SentenceTransformer

# Set up database path
DB_FOLDER = "C:\\Users\\91939\\Downloads\\eng_subtitles_database"
os.makedirs(DB_FOLDER, exist_ok=True)

# Initialize ChromaDB client
client = chromadb.PersistentClient(DB_FOLDER)
collection = client.get_or_create_collection(name="subtitles")

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample subtitles data (replace this with actual subtitle processing logic)
subtitles = {
    "1": "The treasure is buried under the old oak tree.",
    "2": "Adventure awaits those who seek the hidden gold.",
    "3": "A pirate's map will lead you to untold riches."
}

# Store embeddings
for idx, text in subtitles.items():
    embedding = model.encode(text).tolist()
    collection.add(ids=[idx], documents=[text], embeddings=[embedding])

print("✅ All subtitles processed & stored in ChromaDB.")
