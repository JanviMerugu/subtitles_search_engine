import streamlit as st
import os
from vosk import Model, KaldiRecognizer
import wave
import json
from sentence_transformers import SentenceTransformer
import chromadb
from sklearn.metrics.pairwise import cosine_similarity

# Load Vosk model for speech-to-text
def load_vosk_model():
    model_path = "models/vosk_model"  # Make sure this path is correct and the model is downloaded
    model = Model(model_path)
    return model

# Function to transcribe audio to text using Vosk model
def transcribe_audio(audio_path):
    model = load_vosk_model()
    wf = wave.open(audio_path, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    result_text = ""
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            result_text += result_json.get("text", "") + " "
    
    result_text += json.loads(recognizer.FinalResult()).get("text", "")
    return result_text

# Function to preprocess subtitle text and clean it
def preprocess_text(text):
    # Implement any text preprocessing you need like removing timestamps, etc.
    cleaned_text = text.replace("\n", " ").strip()
    return cleaned_text

# Load pre-trained SentenceTransformer for embedding
def load_sentence_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can choose other models as needed
    return model

# Generate embeddings for subtitle text
def generate_embeddings(text, model):
    return model.encode(text)

# Function to load subtitles from the database or JSON file
def load_subtitles():
    # Assuming your subtitles are in JSON format
    subtitle_file_path = "data/subtitles.json"  # Update with the correct path to your subtitles file
    with open(subtitle_file_path, 'r', encoding='utf-8') as file:
        subtitles = json.load(file)
    return subtitles

# Function to create the vector store for ChromaDB (or any database)
def create_vector_store(subtitles, model):
    embeddings = []
    subtitle_texts = []
    
    for subtitle in subtitles:
        cleaned_text = preprocess_text(subtitle["text"])  # Clean the subtitle text
        embedding = generate_embeddings(cleaned_text, model)
        embeddings.append(embedding)
        subtitle_texts.append(cleaned_text)
    
    # Create a ChromaDB vector store or use any database
    # For simplicity, we'll use in-memory storage for this example
    db = chromadb.Client()
    collection = db.create_collection("subtitle_embeddings")
    
    for i, embedding in enumerate(embeddings):
        collection.add(
            documents=[subtitle_texts[i]],
            metadatas=[{"subtitle_id": subtitles[i]["id"]}],
            embeddings=[embedding]
        )
    
    return collection

# Function to search the query against the subtitle embeddings
def search_subtitles(query, collection, model):
    query_embedding = generate_embeddings(query, model)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # Return top 5 results
    )
    
    return results['documents']

# Streamlit UI setup
def main():
    st.set_page_config(page_title="Enhanced Subtitle Search Engine", page_icon="🔍", layout="wide")
    st.title("🎬 Enhanced Subtitle Search Engine")
    st.write("Welcome to the Subtitle Search Engine! Upload your audio query or type a text query to find relevant subtitles.")

    # Text Search Bar for keyword-based search
    search_query = st.text_input("Search Subtitles by Text", placeholder="Enter a keyword, e.g., treasure")

    if search_query:
        # Load subtitle data and model
        subtitles = load_subtitles()
        sentence_model = load_sentence_model()

        # Create vector store if it does not exist
        if not os.path.exists("data/subtitle_embeddings.json"):
            st.write("Creating subtitle embeddings...")
            collection = create_vector_store(subtitles, sentence_model)
            st.write("Subtitle embeddings created and stored!")
        else:
            # Load existing collection from ChromaDB
            collection = chromadb.Client().get_collection("subtitle_embeddings")

        # Search for relevant subtitles based on the keyword
        st.write("Searching for relevant subtitles...")
        search_results = search_subtitles(search_query, collection, sentence_model)
        
        if search_results:
            st.write("Top 5 Relevant Subtitles:")
            for i, result in enumerate(search_results, 1):
                st.write(f"{i}. {result}")
        else:
            st.write("No relevant subtitles found.")

    # File Upload and Audio Transcription Section
    st.subheader("Upload Audio Query")
    uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3", "flac"])

    if uploaded_audio is not None:
        with open("uploaded_audio.wav", "wb") as f:
            f.write(uploaded_audio.getbuffer())
        
        st.audio(uploaded_audio, format='audio/wav')

        # Display a button to start transcription
        if st.button("Transcribe Audio to Text"):
            st.spinner("Transcribing audio...")
            transcribed_text = transcribe_audio("uploaded_audio.wav")
            st.success("Transcription Complete!")
            st.write("Transcribed Text:")
            st.write(transcribed_text)

            # Load subtitle data and model
            subtitles = load_subtitles()
            sentence_model = load_sentence_model()

            # Create vector store if it does not exist
            if not os.path.exists("data/subtitle_embeddings.json"):
                st.write("Creating subtitle embeddings...")
                collection = create_vector_store(subtitles, sentence_model)
                st.write("Subtitle embeddings created and stored!")
            else:
                # Load existing collection from ChromaDB
                collection = chromadb.Client().get_collection("subtitle_embeddings")

            # Search for relevant subtitles based on transcribed query
            if transcribed_text:
                st.write("Searching for relevant subtitles...")
                search_results = search_subtitles(transcribed_text, collection, sentence_model)
                
                if search_results:
                    st.write("Top 5 Relevant Subtitles:")
                    for i, result in enumerate(search_results, 1):
                        st.write(f"{i}. {result}")
                else:
                    st.write("No relevant subtitles found.")
        else:
            st.write("Upload an audio file and click 'Transcribe Audio to Text' to start the search process.")
    
if __name__ == "__main__":
    main()
