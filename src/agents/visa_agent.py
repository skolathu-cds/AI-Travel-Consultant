import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Google Gemini API Key
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API")

def process_query(user_query):
    # Define the endpoint for Google Gemini API
    url = "https://api.google.com/gemini/v1/query"  # Update with the correct endpoint for Gemini API
    
    # Construct the payload for the API request
    payload = {
        "query": user_query,
        "api_key": GEMINI_API_KEY
    }

    # Send the request to Google Gemini API
    response = requests.post(url, json=payload)
    
    # Handle response
    if response.status_code == 200:
        return response.json()['data']['response']
    else:
        return f"Error: Unable to fetch response. Status code {response.status_code}"