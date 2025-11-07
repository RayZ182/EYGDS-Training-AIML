from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

class Prompt(BaseModel):
    topic: str
    question: str

@app.post("/generate")
async def generate_response(prompt: Prompt):
    try:
        response = llm.invoke(f"topic: {prompt.topic}, question: {prompt.question}. Give detailed answer")
        return {"answer": response.content, "model": "mistral/mistral-7b-instruct"}
    except Exception as e:
        return {"error": str(e)}