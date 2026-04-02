import os
import streamlit as st
from groq import Groq

# --- Page Config ---
st.set_page_config(page_title="DSA Chatbot", page_icon="🧠")
st.title("🧠 DSA Chatbot")
st.caption("Ask me anything about Data Structures & Algorithms!")

# --- Load Knowledge Base ---
with open("DSA_Chatbot_Database.txt", "r") as f:
    kb = f.read()

# --- System Prompt ---
system_prompt = f"""
You are a DSA based chatbot. Your job is to provide answers to questions about Data Structures & Algorithms politely.
If there are any questions outside the knowledge base, say you do not have that info.
{kb}
"""

# --- Init Groq Client ---
if "client" not in st.session_state:
    st.session_state.client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# --- Display Chat History ---
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if user_input := st.chat_input("Ask a DSA question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    try:
        response = st.session_state.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.session_state.display_messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)