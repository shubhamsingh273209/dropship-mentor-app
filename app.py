import streamlit as st
import os
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dropship AI Mentor", page_icon="📦")
st.title("📦 Dropship AI Mentor (Cloud Version)")
st.caption("Powered by Llama 3 on Groq")

# --- API SETUP ---
# This looks for the key in Streamlit's secret vault
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.warning("⚠️ API Key not found. Please set it in Streamlit Secrets.")
    st.stop()

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a brutal dropshipping mentor. Concise, strict, and focused on profit margins."}
    ]

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Ask your mentor..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Get AI Response
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=st.session_state.messages,
            temperature=0.7,
        )
        response = completion.choices[0].message.content
        
        # 3. Show AI message
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Error: {e}")