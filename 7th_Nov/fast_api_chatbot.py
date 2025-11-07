# main.py
import json
import os
import threading
from typing import List, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

import google.generativeai as genai  # <-- Use official import
from google.generativeai.types import content_types

# ------------------------------------------------------------------
# 1. Setup
# ------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=api_key)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ------------------------------------------------------------------
# 2. History File Handling
# ------------------------------------------------------------------
HISTORY_FILE = "ga-history.json"
history_lock = threading.Lock()

def load_history() -> List[Dict[str, str]]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            msg for msg in data
            if isinstance(msg, dict) and msg.get("role") in {"user", "assistant"} and "content" in msg
        ]
    except Exception as e:
        print(f"[WARN] History load error: {e}")
        return []

def append_to_history(messages: List[Dict[str, str]]):
    with history_lock:
        existing = load_history()
        existing.extend(messages)
        tmp = f"{HISTORY_FILE}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        os.replace(tmp, HISTORY_FILE)

# ------------------------------------------------------------------
# 3. Convert dict history → Gemini Message objects
# ------------------------------------------------------------------
def dict_to_message(msg_dict: Dict) -> content_types.ContentDict:
    """Convert saved dict to format expected by Gemini chat history."""
    return {
        "role": msg_dict["role"],
        "parts": [msg_dict["content"]]  # 'parts' is required
    }

# Load and convert history
raw_history = load_history()
gemini_history = [dict_to_message(msg) for msg in raw_history]

# Create chat with proper Message format
chat = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=gemini_history)
# Note: Use GenerativeModel().start_chat() — more reliable than client.chats.create

# ------------------------------------------------------------------
# 4. API Model
# ------------------------------------------------------------------
class Prompt(BaseModel):
    query: str

# ------------------------------------------------------------------
# 5. API Endpoint
# ------------------------------------------------------------------
@app.post("/generate")
async def generate_response(prompt: Prompt):
    if not prompt.query or prompt.query.strip() == "":
        raise HTTPException(status_code=400, detail="query cannot be empty or whitespace")

    user_query = prompt.query.strip()

    try:
        # Send message and get response
        response = chat.send_message(user_query)
        assistant_text = response.text

        # Save both user and assistant messages
        user_msg = {"role": "user", "content": user_query}
        assistant_msg = {"role": "assistant", "content": assistant_text}
        append_to_history([user_msg, assistant_msg])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": assistant_text}

# ------------------------------------------------------------------
# 6. Frontend
# ------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
async def get_history():
    return load_history()