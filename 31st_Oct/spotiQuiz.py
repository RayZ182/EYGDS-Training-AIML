import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load your .env file
load_dotenv()

# Map OpenRouter key to what CrewAI expects
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_MODEL"] = "openai/gpt-5-mini"

# --- 2. Define the Agents ---

# Agent 1: Music Analyst
# This agent finds the best songs for a given artist.
song_analyzer_agent = Agent(
    role='Music Analyst',
    goal='Analyze a musician and determine their 3 most critically acclaimed and popular songs.',
    backstory=(
        "You are a seasoned music journalist with deep knowledge of chart history, "
        "critical reception, and fan popularity. Your task is to accurately select "
        "the definitive top 3 songs for any given artist."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent 2: Quiz Master
# This agent takes the song list and creates the "finish the lyrics" quiz.
lyric_generator_agent = Agent(
    role='Quiz Master',
    goal='Create three "finish the lyrics" questions, one for each of the three songs provided.',
    backstory=(
        "You are a fun and creative trivia master specializing in music lyrics. "
        "You must craft challenging and engaging questions by taking an iconic "
        "line from each song's chorus or verse and replacing the last phrase with a blank."
    ),
    verbose=True,
    allow_delegation=False,
)

# --- 3. Define the Tasks ---

# Task 1: Find the top 3 songs
task_1_analyze_artist = Task(
    description=(
        "Search for the artist '{artist_name}' and identify their three definitive "
        "best songs. List the output as a simple comma-separated string of song titles, "
        "for example: 'Song A, Song B, Song C'."
    ),
    expected_output='A comma-separated list of exactly three song titles (e.g., Song A, Song B, Song C).',
    agent=song_analyzer_agent,
)

# Task 2: Generate the quiz questions, using the output of Task 1 as context
task_2_generate_quiz = Task(
    description=(
        "Using the comma-separated list of 3 song titles provided in the context, "
        "generate one 'finish the lyrics' question for each song. "
        "The output must be formatted as a numbered list with the question and the correct answer "
        "in parentheses, like this:\n\n"
        "1. [Song Title]: The lyric is '...finish the sentence, and then... ' \n(Answer: finish the line here).\n\n"
        "2. [Song Title]: The lyric is '...second lyric line...' \n(Answer: second answer here).\n\n"
        "3. [Song Title]: The lyric is '...third lyric line...' \n(Answer: third answer here)."
    ),
    expected_output='A numbered list of three quiz questions in the specified format, including the song title and the correct lyric answer for each.',
    agent=lyric_generator_agent,
    context=[task_1_analyze_artist] # Chains the tasks: Task 2 uses the result of Task 1
)


# --- 4. Setup and Run the Crew ---

# Define the input artist
artist_input = input("Enter a song artist you like: ")

# Create the crew
music_quiz_crew = Crew(
    agents=[song_analyzer_agent, lyric_generator_agent],
    tasks=[task_1_analyze_artist, task_2_generate_quiz],
    verbose=True,
)

# Execute the process
print("--- Starting the Song Quiz Generation Crew ---")
print(f"Artist: {artist_input}\n")

# Use inputs to pass the artist name to the first task
result = music_quiz_crew.kickoff(inputs={'artist_name': artist_input})

print("\n\n################################################")
print("############# Final Quiz Result ################")
print("################################################")
print(result)