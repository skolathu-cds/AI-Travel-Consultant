import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini model without explicitly passing the API key
model = genai.GenerativeModel("gemini-1.5-flash-002", tools="google_search_retrieval")

# Agent for Visa
def process_visa_query(user_query):
    try:
        response = model.generate_content(user_query)  # Use Gemini model to generate content
        rc = response.candidates[0]  # Get the first candidate response
        return rc.content.parts[0].text
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"

# Agent for Air
def process_air_query(user_query):
    try:
        response = model.generate_content(user_query)  # Use Gemini model to generate content
        rc = response.candidates[0]  # Get the first candidate response
        return rc.content.parts[0].text
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"

# Agent for Hotel
def process_hotel_query(user_query):
    try:
        response = model.generate_content(user_query)  # Use Gemini model to generate content
        rc = response.candidates[0]  # Get the first candidate response
        return rc.content.parts[0].text
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"

# Agent for City & Airport
def process_city_airport_query(user_query):
    try:
        response = model.generate_content(user_query)  # Use Gemini model to generate content
        rc = response.candidates[0]  # Get the first candidate response
        return rc.content.parts[0].text
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"

# Utility functions

# Function to re-engineer prompts based on user input
def reengineer_prompt(user_input, context):
    if "visa" in user_input.lower():
        return f"What is the visa requirement for a {context['nationality']} passport holder traveling to {context['destination']} for {context['duration']} weeks?"
    elif "flight" in user_input.lower():
        return f"Provide flight options from {context['origin']} to {context['destination']} for travel dates from {context['start_date']} for {context['duration']} weeks."
    elif "hotel" in user_input.lower():
        return f"List hotels near {context['destination']} for travel dates from {context['start_date']} for {context['duration']} weeks."
    elif "city" in user_input.lower() or "airport" in user_input.lower():
        return f"Provide information on the airport and transport options for {context['destination']}."
    else:
        return user_input  # Default to the original query if not recognized

# Summary generation (mock)
def generate_summary(memory):
    summary = "\n".join([f"User: {item['user_input']}\nSTC: {item['response']}" for item in memory])
    return summary