import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from IPython.display import HTML, Markdown, display


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


# ------------------------------------------------------------
# 2. Initialize the Model using GOOGLE API
# ------------------------------------------------------------
client = genai.Client(api_key=api_key)
chat = client.chats.create(model='gemini-2.0-flash', history=[])


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

    if "last song" in user_input.lower():
        try:
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}")
            continue
        except Exception as e:
            print(f"Last Song cannot be found: {e}")
            continue

    try:
        response = chat.send_message(user_input)
        print("Agent:", response.text)
    except Exception as e:
        print("Error:", e)