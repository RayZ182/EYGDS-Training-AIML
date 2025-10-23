import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---

MODEL_NAME = "deepseek/deepseek-r1-0528:free"
# Retrieve credentials
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

def get_response(userprompt):

    # 2. Initialize LangChain model pointing to OpenRouter
    llm = ChatOpenAI(
        model="deepseek/deepseek-r1-0528:free",
        temperature=0.7,
        max_tokens=512,
        api_key=API_KEY,
        base_url=BASE_URL,
    )

    # 3. Define messages (Mistral models work better with [INST]...[/INST])
    messages = [
        SystemMessage(content="You are a helpful and concise AI Study Assistant"),
        HumanMessage(content= userprompt),
    ]

    # 4. Invoke model and print response
    try:
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        return str(e)

# -------- STREAMLIT UI ------ #

def main():
    st.set_page_config(page_title="AI Study Assistant", layout="centered")

    st.title("🧠 AI Study Assistant")
    st.markdown(f"Using **`{MODEL_NAME}`** via LangChain")
    st.divider()

    # User Input
    user_input = st.text_input(
        "Ask your study question:",
        value = "",
        placeholder="e.g., What are the best methods for memorizing definitions?",
        key="userprompt"
    )

    # Output Display Area
    response_placeholder = st.empty()

    if st.button("Get Advice", type="primary"):
        if not user_input.strip():
            response_placeholder.error("Please enter a question before submitting.")
            return

        with st.spinner('Thinking... Contacting OpenRouter...'):
            # Call the function to get the LLM response
            assistant_response = get_response(user_input)

        # Display the response
        if assistant_response.startswith("❌ ERROR") or assistant_response.startswith("**Error:**"):
            response_placeholder.error(assistant_response)
        else:
            response_placeholder.success("Assistant Response:")
            st.markdown(assistant_response)

if __name__ == "__main__":
    main()
