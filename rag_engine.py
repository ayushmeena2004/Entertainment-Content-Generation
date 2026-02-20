import os
import time
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Persistent ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="entertainment_context")

def add_character_to_db(name, description):
    """Saves character details into ChromaDB."""
    try:
        unique_id = f"{name}_{int(time.time())}"
        collection.add(
            documents=[description],
            metadatas=[{"name": name}],
            ids=[unique_id]
        )
        return f"Successfully saved '{name}' to memory!"
    except Exception as e:
        return f"Error saving to DB: {str(e)}"

def get_all_characters():
    """Retrieves all stored characters for the UI preview."""
    try:
        results = collection.get()
        characters = []
        for doc, meta in zip(results['documents'], results['metadatas']):
            characters.append({"Name": meta['name'], "Description": doc})
        return characters
    except Exception:
        return []

def clear_all_memory():
    """Wipes the database."""
    try:
        all_ids = collection.get()['ids']
        if all_ids:
            collection.delete(ids=all_ids)
            return "Memory wiped successfully!"
        return "Memory is already empty."
    except Exception as e:
        return f"Error: {str(e)}"

def generate_script(scene_topic, tone, retries=3, delay=5):
    """Generates script using RAG with a retry loop."""
    # 1. Retrieve Context
    results = collection.query(query_texts=[scene_topic], n_results=3)
    docs = results.get('documents', [[]])[0]
    context_text = "\n".join(docs) if docs else "No specific character context found."

    # 2. Build Prompt
    prompt = (
        f"Role: Professional Screenwriter. \n"
        f"Tone: {tone}. \n"
        f"Context from Memory: {context_text} \n"
        f"Task: Write a script scene about: {scene_topic}"
    )

    # 3. Generate with Retry (Gemini 2.5 Flash)
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(delay)
                continue
            return f"Error: {str(e)}"