from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Pydantic Class
class Query(BaseModel):
    topic: str
    question: str

# OpenRouter configuration
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("OPENROUTER_API_KEY")

# POST Request
@app.post("/generate")
async def generate(request: Query):
    prompt = f"Topic: {request.topic}\nQuestion: {request.question}\nProvide a detailed answer:"

    # preparing the payload
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    #headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Capstone Project"
    }

    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"].strip()

        return {"answer": answer, "model": "mistralai/mistral-7b-instruct"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))