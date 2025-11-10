from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from datetime import datetime
import logging
import re

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.FileHandler('chats.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    logger.error("OPENROUTER_API_KEY not found in environment variables")
    raise RuntimeError("OPENROUTER_API_KEY is required")

# Initialize LLM
try:
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        temperature=0.4,
        max_tokens=256,
        api_key=api_key,
        base_url=base_url
    )
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise

# TOOLS
def current_date() -> str:
    return datetime.today().strftime("%Y-%m-%d")

def current_time() -> str:
    return datetime.today().strftime("%H:%M:%S")

def reverse_string(text: str):
    return text[::-1].strip()


# === OUTPUT CLEANER ===
def clean_response(text: str) -> str:
    """
    Remove common unwanted tokens/artifacts from Mistral or similar model outputs.
    """
    if not text:
        return text

    # Remove common XML-like tags, INST tags, extra brackets, etc.
    cleaners = [
        r"</?s>",
        r"<s>",
        r"</s>",
        r"\[/?INST\]",
        r"\[/?INST\]",
        r"<\s*/?inst\s*>",
        r"\[",
        r"\]",
        r"^\W+|\W+$",  # leading/trailing non-word chars
    ]

    cleaned = text
    for pattern in cleaners:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Clean up extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


# Pydantic Model
class Prompt(BaseModel):
    question: str

# POST Method
@app.post("/ask")
async def ask(prompt: Prompt):
    user_question = prompt.question.strip()

    if not user_question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"User: {user_question}")

    try:
        response_content = None

        # Tool 1
        if "current date" in user_question.lower():
            curr_date = current_date()
            response = curr_date
            response_content = clean_response(response)

        # Tool 2
        elif "current time" in prompt.question.lower():
            curr_time = current_time()
            response = curr_time
            response_content = clean_response(response)

        # Tool 3
        elif "reverse" in prompt.question.lower():
            parts = prompt.question.split()
            sent = " ".join(parts[1:])
            response = f"The reversed string of '{sent}' is '{reverse_string(sent)}'."
            response_content = clean_response(response)

        # General QnA
        else:
            response = llm.invoke(prompt.question)
            response_content = clean_response(response.content)

        if response_content is None:
            response_content = "Sorry , I couldn't process it."

        logger.info(f"Agent: {response_content}")
        return {"Agent": response_content}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while processing your request")