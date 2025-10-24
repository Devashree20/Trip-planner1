# backend.py
import os
from datetime import datetime
from serpapi import GoogleSearch
from dotenv import dotenv_values
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# Load environment variables
config = dotenv_values(".env")
SERPAPI_KEY = config.get("SERPAPI_KEY")
GEMINI_API_KEY = config.get("GEMINI_API_KEY")
SERPERDEV_API_KEY = config.get("SERPERDEV_API_KEY")

os.environ["SERPER_API_KEY"] = SERPERDEV_API_KEY

# Initialize Gemini LLM for CrewAI
my_llm = LLM(
    model="gemini/gemini-2.5-pro",
    api_key=GEMINI_API_KEY
)

def fetch_flights(source, destination, departure_date, return_date):
    """Fetch flight information using SerpAPI."""
    try:
        params = {
            "engine": "google_flights",
            "departure_id": source,
            "arrival_id": destination,
            "outbound_date": str(departure_date),
            "return_date": str(return_date),
            "currency": "INR",
            "hl": "en",
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    except Exception as e:
        return {"error": str(e)}


def extract_cheapest_flights(flight_data):
    """Extract the cheapest 3 flights from flight_data."""
    if not isinstance(flight_data, dict):
        return []
    best_flights = flight_data.get("best_flights", [])
    return sorted(best_flights, key=lambda x: x.get("price", float("inf")))[:3]


def format_datetime(iso_string):
    """Format time for display."""
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%b-%d, %Y | %I:%M %p")
    except:
        return "N/A"


def generate_itinerary(destination, num_days, travel_theme, activity_preferences, budget):
    """Use CrewAI to create a travel plan."""
    search_tool = SerperDevTool()

    # Define Agents
    researcher = Agent(
        role="Travel Researcher",
        goal=f"Gather detailed info on {destination}",
        backstory="Expert travel analyst for destinations, culture, safety, and climate.",
        llm=my_llm,
        tools=[search_tool],
        verbose=True
    )

    planner = Agent(
        role="Itinerary Planner",
        goal=f"Create a {num_days}-day itinerary for {destination}",
        backstory="Meticulous travel planner crafting day-by-day schedules.",
        llm=my_llm,
        verbose=True
    )

    hotel_expert = Agent(
        role="Accommodation & Dining Expert",
        goal=f"Find the best hotels and restaurants in {destination}",
        backstory="Concierge expert in hotels and restaurants.",
        llm=my_llm,
        tools=[search_tool],
        verbose=True
    )

    # Tasks
    research_task = Task(
        description=f"Research top attractions and local info for {destination}.",
        agent=researcher,
        expected_output="Detailed markdown summary of attractions and culture."
    )

    hotel_task = Task(
        description=f"Find top-rated hotels and restaurants based on {budget} budget.",
        agent=hotel_expert,
        expected_output="List of best hotels and restaurants with brief details."
    )

    plan_task = Task(
        description=f"Create a {num_days}-day itinerary using previous research for a {travel_theme} trip.",
        agent=planner,
        expected_output="Structured day-by-day itinerary."
    )

    # Crew execution
    crew = Crew(
        agents=[researcher, hotel_expert, planner],
        tasks=[research_task, hotel_task, plan_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result
