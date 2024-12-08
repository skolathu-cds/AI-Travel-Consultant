import openai
import logging
from dotenv import load_dotenv
import os
from travel_tools import (
    get_visa_details, get_flight_details, get_hotel_details, get_city_airport_info
)
from travel_prompts import visa_prompt_template, flight_prompt_template, hotel_prompt_template, city_prompt_template

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize logging
logger = logging.getLogger(__name__)

def reformulate_query(query, template):
    """Reformulate the user's query using OpenAI."""
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # You can replace this with other models like "text-davinci-003"
            prompt=template.format(query=query),
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error during query reformulation: {e}")
        return "Error reformulating the query."

def decide_tool_to_invoke(query):
    """Decide which tool to invoke based on the user's query."""
    if "visa" in query.lower():
        return "visa"
    elif "flight" in query.lower():
        return "flight"
    elif "hotel" in query.lower():
        return "hotel"
    elif "airport" in query.lower() or "city" in query.lower():
        return "city"
    else:
        return None

def generate_response(query):
    """Generate a response based on the user query."""
    try:
        # Reformulate the query using OpenAI
        if "visa" in query.lower():
            reformulated_query = reformulate_query(query, visa_prompt_template)
            nationality, residence, duration = "Indian", "India", 14  # Example extraction
            return get_visa_details(nationality, residence, duration)
        elif "flight" in query.lower():
            reformulated_query = reformulate_query(query, flight_prompt_template)
            return get_flight_details("Mumbai", "Paris", "2024-12-15", "2024-12-29")
        elif "hotel" in query.lower():
            reformulated_query = reformulate_query(query, hotel_prompt_template)
            return get_hotel_details("Paris", "2024-12-15", "2024-12-29", 1)
        elif "city" in query.lower() or "airport" in query.lower():
            reformulated_query = reformulate_query(query, city_prompt_template)
            return get_city_airport_info("Paris")
        else:
            return "I can help with visa, flight, hotel, and city information. Please clarify your request."
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "There was an error processing your request. Please try again."
