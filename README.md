Project Overview:
Most AI generators produce "novel-style" paragraphs. ProScript AI is different. It is hard-coded to think like a Hollywood Script Doctor. By combining ChromaDB (vector memory) with Gemini 2.5 Flash, the system retrieves specific character traits—like a character's nervous tics or unique dialogue patterns—and weaves them into a perfectly formatted script.

Key Capabilities
Vertical Dialogue Stacking: Automatically formats scripts with character names centered (on their own line) and dialogue below, mimicking real-world film scripts.

Persistent Character Memory: Uses a RAG pipeline to store and retrieve "Character Bibles." If you define a character once, the AI remembers them forever.

Multi-Scene Logic: Generates complex, multi-location narratives in a single output.

Production-Ready UI: A sleek Streamlit interface designed for rapid creative iteration.


Technical Stack:

Component          Technology
LLM                Google Gemini 2.5 Flash (2026 SDK)
Vector Database    ChromaDB
Framework          Python 3.10
Frontend           Streamlit
Orchestration      Custom RAG Logic with Exponential Backoff (429 handling)

PROJECT STRUCTURE:
DATAGAMI PROJECT/
├── app.py              # Streamlit Web Interface (UI Logic)
├── rag_engine.py       # ChromaDB Querying & Gemini API Integration
├── .env                # Secret API Keys (Git-ignored)
├── requirements.txt    # Project Dependencies
└── README.md           # Project Documentation

Setup & Installation

1. Clone the Repository
git clone https://github.com/ayushmeena2004/Entertainment-Content-Generation

2. Configure Environment
Create a .env file in the root directory:
Plaintext
GOOGLE_API_KEY=your_api_key_here

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
streamlit run app.py


