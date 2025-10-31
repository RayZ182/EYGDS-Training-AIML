import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


# ------------------------------------------------------------
# 2. Initialize the Mistral model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

def song_artist(prompt):
    response = llm.invoke(f"Who played the song{prompt}? Response with only the artist name")
    return response.content

def similar_artist(prompt):
    artist = song_artist(prompt)
    response = llm.invoke(f"Give 5 artist as bullet points similar to {artist}.")
    return response.content

# ------------------------------------------------------------
# 5. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    if user_input.lower().startswith("artist"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[2:])
            response = song_artist(sent)
            print(f"Agent: {response}")
            continue
        except Exception as e:
            print(f"Agent: Artist not found: {e}")
            continue

    if user_input.lower().startswith("suggest"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = similar_artist(sent)
            print(f"Agent: {response}")
            continue
        except Exception as e:
            print(f"Agent: Similar Songs not found: {e}")
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
    except Exception as e:
        print("Error:", e)
