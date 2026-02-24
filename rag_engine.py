import os
import time
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="entertainment_context")

def add_character_to_db(name, description):
    
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
   
    try:
        results = collection.get()
        characters = []
        for doc, meta in zip(results['documents'], results['metadatas']):
            characters.append({"Name": meta['name'], "Description": doc})
        return characters
    except Exception:
        return []

def clear_all_memory():
   
    try:
        all_ids = collection.get()['ids']
        if all_ids:
            collection.delete(ids=all_ids)
            return "Memory wiped successfully!"
        return "Memory is already empty."
    except Exception as e:
        return f"Error: {str(e)}"

def generate_script(scene_topic, tone, retries=3, delay=5):
    
  
    results = collection.query(query_texts=[scene_topic], n_results=5)
    docs = results.get('documents', [[]])[0]
    context_text = "\n".join(docs) if docs else "No specific character context found. Use industry archetypes."

  
    prompt = (
        f"ROLE: Professional Hollywood Screenwriter and Script Doctor.\n\n"
        f"TASK: Write a complete, multi-scene script based on: {scene_topic}.\n\n"
        f"CONTEXT FROM CHARACTER DATABASE:\n{context_text}\n\n"
        f"TONE: {tone}\n\n"
        f"STRICT FORMATTING RULES (MANDATORY):\n"
        f"1. SCENES: Generate the entire story segment in one response. Use 'SCENE 1', 'SCENE 2', etc.\n"
        f"2. SLUGLINES: Every new location must start with a bold line: **INT. LOCATION - TIME**.\n"
        f"3. ACTION: Present tense, vivid, max 3 lines per block. Focus on character tics found in context.\n"
        f"4. VERTICAL DIALOGUE (REAL FILM FORMAT):\n"
        f"   - CHARACTER NAME in ALL CAPS on its own line.\n"
        f"   - Parenthetical (e.g., emotional cue) on its own line BELOW the name.\n"
        f"   - Dialogue on its own line BELOW the parenthetical.\n"
        f"5. NO QUOTATION MARKS: Do not use quotes around speech.\n"
        f"6. WHITE SPACE: Add a blank line between different character turns and action blocks.\n"
        f"7. TRANSITION: End the entire script with 'FADE OUT.'\n\n"
        f"VERTICAL FORMAT EXAMPLE:\n"
        f"CHARACTER NAME\n"
        f"(emotional cue)\n"
        f"This is how the dialogue should look.\n"
    )

  
    for attempt in range(retries):
        try:
            # Use the most stable 2026 model for complex formatting
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            
            if response.text:
                return response.text
            return "Error: The model returned an empty response."

        except Exception as e:
            # Handle Quota (429) or Network errors
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(delay)
                continue
            return f"Generation Error: {str(e)}"
