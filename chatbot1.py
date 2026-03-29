import ssl
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()
import os
os.environ["GRPC_DNS_RESOLVER"] = "native"
import streamlit as st
from google import genai

# --- Page Config ---
st.set_page_config(page_title="DSA Chatbot", page_icon="🧠")
st.title("🧠 DSA Chatbot")
st.caption("Ask me anything about Data Structures & Algorithms!")

# --- Load Knowledge Base ---
with open("DSA_Chatbot_Database.txt", "r") as f:
    kb = f.read()

# --- System Prompt ---
system_prompt = f"""
you are a DSA based chatbot your job is to provide answers to the questions asked by the users,
you should answer them in polite, if there is any questions out of the kb say you did not have that info, only refer the kb and provide the response. 

{kb}
"""

# --- Init client and chat in session state (persists across reruns) ---
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key="API_KEY")  # <-- Replace with your API key

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_prompt}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if user_input := st.chat_input("Ask a DSA question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    response = st.session_state.chat.send_message(user_input)
    bot_reply = response.text

    # Show bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)