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
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

def word_count(phrase):
    parts = phrase.split()
    count = len(parts) - 1
    return count

def reverse_text(phrase):
    parts = phrase.split()
    sent = parts[1:][::-1]
    rev = ' '.join(sent)
    return rev

def vocab(phrase):
    parts = phrase.split()
    sent = " ".join(parts[1:])
    response = llm.invoke(f"Give a synonym and also the meaning of : {sent}")
    return str(response.content)

def casing(phrase):
    parts = phrase.split()
    sent = " ".join(parts[1:])
    if parts[0].lower() == "upper":
        sent = sent.upper()
    elif parts[0].lower() == "lower":
        sent = sent.lower()
    return sent

def repeater(phrase):
    parts = phrase.split()
    word = parts[1]
    count = int(parts[2])
    return f"{word} " * count


# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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

    # Calling the Tools

    # Word Counter Tool
    if user_input.lower().startswith("count"):
        try:
            response = word_count(user_input)
            print(f"Agent: Your sentence has {response} words.")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Word count cannot be processed: {e}")
            continue

    # Reverse Text Tool
    if user_input.lower().startswith("reverse"):
        try:
            response = reverse_text(user_input)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Reverse text cannot be processed: {e}")
            continue

    # Vocabulary helper Tool
    if user_input.lower().startswith("define"):
        try:
            response = vocab(user_input)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Vocab helo cannot be given: {e}")
            continue

    # Uppercase / Lowercase Tool
    if user_input.lower().startswith("case"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = casing(sent)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Casing cannot be processed: {e}")

    # Word Repeater Tool
    if user_input.lower().startswith("repeat"):
        try:
            response = repeater(user_input)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Repeating cannot be processed: {e}")
            continue

    # HISTORY
    if user_input.lower() == "history":
        try:
            messages = memory.load_memory_variables({}).get("chat_history", [])
            for i, message in enumerate(messages):
                print(f"Agent: {message}")
                continue
        except Exception as e:
            print(f"Agent: History cannot be accessed: {e}")
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)