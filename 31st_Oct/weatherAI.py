import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import litellm

# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ---------------------------------------------------------------------
# 2. Configure LiteLLM globally for OpenRouter
# ---------------------------------------------------------------------
litellm.api_key = os.getenv("OPENROUTER_API_KEY")
litellm.api_base = "https://openrouter.ai/api/v1"
model_name = "openrouter/mistralai/mistral-7b-instruct"

# Helper Function to get the weather data
def fetch_weather(city:str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
    "City": data['name'],
    "Country": data['sys']['country'],
    "Temperature": f"{data['main']['temp']}C",
    "Feels like": f"{data['main']['feels_like']}C",
    "Humidity": f"{data['main']['humidity']}%",
    "Wind Speed": f"{data['wind']['speed']} m/s",
    "Weather": data['weather'][0]['main'],
    "Description": data['weather'][0]['description']
}
    except Exception as e:
        print(f"Weather Cannot be fetched: {e}")

# print(fetch_weather(city="London"))
# Get the city
user_city = str(input("Enter City: "))
# Defining Agents
# Agent 1 - Weather Summarizer
weather_summarizer = Agent(
    role="Summarizer",
    goal=f"""Create a summary of the weather conditions from the given data:
        {fetch_weather(user_city)}    
    """,
    backstory="A helpful and professional Weather Agent",
    allow_delegation=True,
    llm=model_name,
)

# Agent 2 - Clothes Suggestor
clothes = Agent(
    role = "Give Clothing Suggestion",
    goal = "Give clothing suggestion based on the summary of the weather and what items to bring according to the weather conditions",
    backstory="A helpful and knowledgeable Agent with knowledge about the weather conditions",
    allow_delegation=True,
    llm=model_name
)

# Specifying the task
current_weather_data = fetch_weather(user_city)
summarize_task = Task(
    description="Analyze the given the weather data and create a summary of the weather conditions",
    expected_output="A brief yet simple summary of the weather conditions",
    agent=weather_summarizer
)

clothes_needed = Task(
    description="Take the summarizer's summary of the weather and recommend clothing items to wear and other accessories to bring according to the weather conditions",
    expected_output="Concise bullet points with a very short reason",
    agent=clothes
)

# Configure the Crew
crew = Crew(
    agents=[weather_summarizer, clothes],
    tasks=[summarize_task, clothes_needed],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    topic = "Creating a Weather summary and clothing recommendations for that weather"
    print(f"\n--- Running CrewAI Planner–Specialist Workflow ---\nTopic: {topic}\n")
    result = crew.kickoff(inputs={"topic": topic})
    print("\n--- FINAL OUTPUT ---\n")
    print(result)