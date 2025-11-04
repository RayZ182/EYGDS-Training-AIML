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
def research(phrase):
    response = llm.invoke(f"Research on the topic {phrase}")
    return response.content


def notifier(summary, filename = "summary.txt"):
    try:
        with open(filename, "w") as f:
            f.write(summary)
        return f"Summary written to {filename}"
    except Exception as e:
        return f"Error in notifying: {e}"

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

    # handle summarizer
    if user_input.lower().startswith("research"):
        try:
            parts = user_input.split()
            sent = " ".join(parts[1:])
            res = research(sent)
            print("Agent: Research completed")
            summ = summarize(res)
            print("Agent: Summary completed")
            noti = notifier(summ)
            print(f"Agent: Research and Summary completed on topic {sent}")
        except Exception as e:
            print(f"Error: {e}")
    # try:
    #     response = llm.invoke(user_input)
    #     print("Agent:", response.content)
    #     memory.save_context({"input": user_input}, {"output": response.content})
    # except Exception as e:
    #     print("Error:", e)

