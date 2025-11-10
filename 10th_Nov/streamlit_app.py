import streamlit as st
import requests
import json
from datetime import datetime

# === CONFIG ===
FASTAPI_URL = "http://localhost:8000/ask"  # Change if deployed
TIMEOUT = 30

# === STREAMLIT PAGE CONFIG ===
st.set_page_config(
    page_title="QnA Bot",
    page_icon="robot",
    layout="centered"
)

st.title("QnA Bot with Tools")
st.caption("Ask about date, time, reverse strings, or anything!")

# === SESSION STATE FOR CHAT HISTORY ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === DISPLAY CHAT HISTORY ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# === USER INPUT ===
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    FASTAPI_URL,
                    json={"question": prompt},
                    timeout=TIMEOUT
                )

                if response.status_code == 200:
                    data = response.json()
                    agent_response = data.get("Agent", "No response")
                    st.markdown(agent_response)
                    st.session_state.messages.append({"role": "assistant", "content": agent_response})
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.Timeout:
                error_msg = "Request timed out. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to the backend. Is the FastAPI server running?"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# === SIDEBAR INFO ===
with st.sidebar:
    st.header("About")
    st.write("This bot supports:")
    st.write("- `current date`")
    st.write("- `current time`")
    st.write("- `reverse hello`")
    st.write("- General Q&A")

    st.header("Backend")
    st.write("FastAPI server must be running at:")
    st.code(FASTAPI_URL, language="text")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()