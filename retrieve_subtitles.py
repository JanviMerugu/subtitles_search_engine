import chromadb
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

# Load the same embedding model used for subtitles
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB collection
chroma_client = chromadb.PersistentClient(path="chromadb")  # Adjust path if needed
collection = chroma_client.get_collection("subtitle_embeddings")

def retrieve_subtitles(query_text, top_n=5):
    """
    Retrieve the top matching subtitle segments for a given query.
    
    Args:
        query_text (str): The text query (from transcribed audio).
        top_n (int): Number of results to return.
    
    Returns:
        List of tuples (subtitle_text, similarity_score)
    """
    if not query_text:
        print("❌ Error: Empty query text. Please provide a valid query.")
        return []

    # Convert query text into an embedding
    query_embedding = model.encode(query_text, normalize_embeddings=True)

    # Fetch stored subtitle embeddings from ChromaDB
    subtitle_embeddings = collection.get(include=["embeddings"])
    subtitle_texts = collection.get(include=["documents"])

    # Compute similarity scores
    similarities = [1 - cosine(query_embedding, emb) for emb in subtitle_embeddings["embeddings"]]

    # Rank results based on similarity
    sorted_indices = np.argsort(similarities)[::-1]  # Descending order
    top_results = [(subtitle_texts["documents"][i], similarities[i]) for i in sorted_indices[:top_n]]

    return top_results

if __name__ == "__main__":
    # Example: Replace this with actual transcribed text
    transcribed_query = "I love movies and acting."

    print("🔍 Retrieving top subtitle matches...")
    results = retrieve_subtitles(transcribed_query)

    # Print results
    for i, (subtitle, score) in enumerate(results):
        print(f"{i+1}. Score: {score:.4f} | Subtitle: {subtitle}")
