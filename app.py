import streamlit as st
import rag_engine as brain
import pandas as pd

st.set_page_config(page_title="ScriptCraft", layout="wide")

st.markdown("""
    <style>
    /* Force Courier font for the entire app to mimic a typewriter */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Courier Prime', monospace;
    }

    /* Style the code block specifically for the script output */
    .stCodeBlock {
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
        padding: 20px !important;
        color: #000000 !important;
    }

    /* Optional: Make the text area look more like a script page */
    textarea {
        font-family: 'Courier Prime', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 ScriptCraft: Entertainment Content Generator")
st.markdown("Build your character universe and generate scripts using **Gemini 2.5 Flash**.")

col1, col2 = st.columns([1, 2])

# --- LEFT COLUMN: CHARACTER MANAGEMENT ---
with col1:
    st.header("1. Character Memory")
    
    with st.expander("➕ Add New Character", expanded=True):
        char_name = st.text_input("Name")
        char_desc = st.text_area("Backstory / Personality")
        if st.button("Save to Memory"):
            if char_name and char_desc:
                msg = brain.add_character_to_db(char_name, char_desc)
                st.success(msg)
                st.rerun() # Refresh to show in table
            else:
                st.error("Fields cannot be empty.")

    st.subheader("📜 Active Memory")
    chars = brain.get_all_characters()
    if chars:
        st.table(pd.DataFrame(chars))
        if st.button("🗑️ Clear All Memory"):
            msg = brain.clear_all_memory()
            st.warning(msg)
            st.rerun()
    else:
        st.caption("No characters in memory yet.")

# --- RIGHT COLUMN: GENERATION ---
with col2:
    st.header("2. Script Generator")
    
    topic = st.text_area("What happens in this scene?", height=150, 
                         placeholder="Example: Miller finds a mysterious letter in his locker...")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        tone = st.selectbox("Tone", ["Dramatic", "Comedic", "Noir", "Thriller", "Horror"])
    
    if st.button("🚀 Generate Script", use_container_width=True):
        if topic:
            with st.spinner("Retrieving character data & writing..."):
                script = brain.generate_script(topic, tone)
                st.subheader("Generated Script")
                st.markdown(script)
                st.download_button("📩 Download as Markdown", script, file_name="scene.md")
        else:
            st.warning("Please describe the scene first.")