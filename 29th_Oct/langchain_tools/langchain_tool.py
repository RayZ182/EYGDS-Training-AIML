import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage


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

# Summarizer Tool
def summarize(phrase):
    response = llm.invoke(f"Summarize {phrase} in 60 words")
    return response.content

# Task classifier
def classify_task(phrase):
    response = llm.invoke(f"Classify the task as HIGH, MEDIUM or LOW Priority: {phrase}. Give only the priority as output.")
    return response.content

# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
note_memory = ConversationBufferMemory(memory_key="note_history", return_messages=True)

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

    # handle summarizer
    if user_input.lower().startswith("summarize"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = summarize(sent)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Summary cannot be generated: {e}")
            continue

    # sentiment analyzer
    if user_input.lower().startswith("analyze"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = llm.invoke(f"Analyze the sentiment of the phrase: {sent}. Give result as Positive, Neutral or Negative. Also concisely specify the aspect")
            print(f"Agent: {response.content}")
            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Sentiment cannot be determined: {e}")
            continue

    # Note Maker
    if user_input.lower().startswith("note"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = llm.invoke(f"Remind me to {sent}")
            print(f"Agent: Noted: {response.content}")
            note_memory.save_context({"input": user_input}, {"output": str(sent)})
            continue
        except Exception as e:
            print(f"Agent: Note cannot be Processed: {e}")
            continue
    if user_input.lower() == "get notes":
        try:
            messages = note_memory.load_memory_variables({}).get("note_history", [])
            note_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
            if note_messages:
                note_count = len(note_messages)

                print(f"Agent: You currently have {note_count} note")
                for i, message in enumerate(note_messages):
                    print(f"  Note {i + 1}: {message.content}")
            else:
                print("Agent: No notes present")
            continue
        except Exception as e:
            print(f"Agent: Note cannot be Processed: {e}")
            continue

    # Text Improver
    if user_input.lower().startswith("improve"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = llm.invoke(f"Rewrite text to make it clearer or more professional: {sent} ")
            memory.save_context({"input": user_input}, {"output": str(response.content)})
            print(f"Agent: {response.content}")
            continue
        except Exception as e:
            print(f"Agent: Rewrite text cannot be processed: {e}")

    # Task Priority Classifier
    if user_input.lower().startswith("priority"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            response = classify_task(sent)
            if "high" in response.lower():
                print(f"Agent: Task '{sent}' marked as HIGH Priority")
            elif "medium" in response.lower():
                print(f"Agent: Task '{sent}' marked as MEDIUM Priority")
            elif "low" in response.lower():
                print(f"Agent: Task '{sent}' marked as LOW Priority")

            memory.save_context({"input": user_input}, {"output": str(response)})
            continue
        except Exception as e:
            print(f"Agent: Task cannot be processed: {e}")
