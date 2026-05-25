import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import sys
sys.path.append('src')
from hybrid_retriever import HybridRetriever

load_dotenv()

st.set_page_config(page_title="Goodreads Chatbot", page_icon="📚", layout="wide")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'retriever' not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        retriever = HybridRetriever()
        retriever.load_qa_dataset('data/processed/qa_dataset.csv')
        retriever.create_qa_collection()
        st.session_state.retriever = retriever

with st.sidebar:
    st.header("📚 Goodreads Self-Help Chatbot")
    st.write("Ask questions about self-help books!")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.title("📚 Self-Help Book Chatbot")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])
            if "source" in message:
                st.caption(f"📖 Source: {message['source']}")

# User input
user_input = st.chat_input("Ask about self-help books...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    # Search for relevant Q/A
    retriever = st.session_state.retriever
    search_result = retriever.hybrid_search(user_input)
    context = search_result['answer']
    
    # Generate response with Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    system_prompt = "You are a helpful assistant answering questions about self-help books. Keep answers concise and helpful."
    user_message = f"User asked: {user_input}\n\nContext: {context}\n\nAnswer based on the context:"
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_message}],
        temperature=1,
        max_tokens=500,
    )
    
    response = completion.choices[0].message.content
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "source": search_result['source_book']
    })
    
    with st.chat_message("assistant"):
        st.write(response)
        st.caption(f"📖 Source: {search_result['source_book']}")
    
    st.rerun()
