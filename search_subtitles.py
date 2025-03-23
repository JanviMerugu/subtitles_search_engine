import chromadb
from sentence_transformers import SentenceTransformer
import os

# ✅ Load the Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ✅ Set up the database path
DB_FOLDER = "C:\\Users\\91939\\Downloads\\eng_subtitles_database"
client = chromadb.PersistentClient(DB_FOLDER)

# ✅ Load the collection
collection = client.get_or_create_collection("subtitles")

# ✅ Debug: Check if database contains subtitles
print(f"🔍 Debug: Number of stored subtitles → {collection.count()}")

def search_subtitles(query):
    """Search for the most relevant subtitle based on user query."""
    query_embedding = model.encode(query, convert_to_tensor=True).tolist()

    # ✅ Debug: Print query embedding
    print(f"🔎 Debug: Query Embedding → {query_embedding[:5]}... (truncated)")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # Return top 5 most relevant results
    )

    # ✅ Debug: Print retrieved results
    print("🔍 Debug: Retrieved Results →", results)

    if not results["documents"] or not results["documents"][0]:
        return ["❌ No relevant subtitles found. Try a different query."]

    return results["documents"][0]  # Return the top 5 matched subtitles

if __name__ == "__main__":
    while True:
        query = input("\n🔎 Enter search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("👋 Exiting...")
            break
        
        results = search_subtitles(query)
        print("\n🔍 **Search Results:**")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result}")
