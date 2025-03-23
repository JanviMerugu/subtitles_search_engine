import os
import re
import chromadb
import glob
from sentence_transformers import SentenceTransformer

# Update paths based on your project structure
SUBTITLES_FOLDER = r"C:\Users\91939\Desktop\subtitle_search_engine\dataset\subtitles"
DB_FOLDER = r"C:\Users\91939\Desktop\subtitle_search_engine\dataset\chroma_db"  # ✅ Fixed to be a directory

# Ensure ChromaDB directory exists
os.makedirs(DB_FOLDER, exist_ok=True)  

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
client = chromadb.PersistentClient(DB_FOLDER)  # ✅ This will now correctly use a directory
collection = client.get_or_create_collection("subtitles")

def clean_subtitle(text):
    """Removes timestamps and special characters from subtitle files."""
    text = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", text)  # Remove timestamps
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text.strip()

def process_subtitles():
    """Reads, cleans, and indexes subtitle files into ChromaDB."""
    subtitle_files = glob.glob(os.path.join(SUBTITLES_FOLDER, "*.srt"))

    for file in subtitle_files:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
            cleaned_text = clean_subtitle(raw_text)

            # Convert to embedding
            embedding = model.encode(cleaned_text, show_progress_bar=False).tolist()

            # Store in ChromaDB
            collection.add(
                documents=[cleaned_text],
                embeddings=[embedding],
                metadatas=[{"filename": os.path.basename(file)}],
                ids=[os.path.basename(file)]
            )
            print(f"✅ Indexed: {file}")

    print("\n✅ All subtitles processed & stored in ChromaDB.")

if __name__ == "__main__":
    process_subtitles()
