import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define a dynamic ChatPromptTemplate
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a Summarizer and a exceptional Quiz Master. Create a Summary on {topic} under 60 words and generate three questions on {topic} for a Quiz. Do not generate answers [/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()

# 4. Create a Reusable Chain (Prompt -> Model -> Output)
def generate_explanation(topic):
    chain = prompt | llm | parser
    response = chain.invoke({"topic": topic})
    return response


# 5. Run Dynamically for any topic
user_topic = input("Enter a topic you want: ").strip()
response = generate_explanation(user_topic)

print("\n--- Mistral Response ---")
print(response)

# 6. Log the prompt and output
os.makedirs("logs",exist_ok=True)
log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "topic": user_topic,
    "response": response
}

with open("logs/sequential_chain_log.jsonl", "a", encoding = "utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")

print("\nResponse logged to logs/sequential_chain_log.jsonl")