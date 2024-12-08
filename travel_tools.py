import google.generativeai as genai
import requests
import logging
import traceback

logger = logging.getLogger(__name__)

# Configure Google Generative AI
genai.configure(api_key="GOOGLE_API_KEY")

# Google Generative AI-based tools
def get_visa_details(nationality, residence_country, travel_duration):
    """Fetch visa details using Google's Generative AI."""
    try:
        query = f"Visa requirements for a {nationality} residing in {residence_country} for a trip lasting {travel_duration} days."
        response = genai.generate_text(prompt=query)
        return response['candidates'][0]['output']  # Adjust based on actual response structure
    except Exception as e:
        logger.error(f"Error fetching visa details: {traceback.format_exc()}")
        return "Unable to fetch visa details. Please try again."

def get_tourist_destinations(city):
    """Fetch tourist destinations using Google's Generative AI."""
    try:
        query = f"Top tourist destinations in {city}."
        response = genai.generate_text(prompt=query)
        return response['candidates'][0]['output']
    except Exception as e:
        logger.error(f"Error fetching tourist destinations: {traceback.format_exc()}")
        return "Unable to fetch tourist destinations. Please try again."

def get_city_airport_info(city):
    """Fetch city and airport agent details using Google's Generative AI."""
    try:
        query = f"Airport agents and services available in {city}."
        response = genai.generate_text(prompt=query)
        return response['candidates'][0]['output']
    except Exception as e:
        logger.error(f"Error fetching city and airport info: {traceback.format_exc()}")
        return "Unable to fetch airport information. Please try again."

def get_hotel_details(destination, check_in, check_out, travelers):
    """Fetch hotel options using Google's Generative AI."""
    try:
        query = f"Hotels in {destination} for {travelers} travelers from {check_in} to {check_out}."
        response = genai.generate_text(prompt=query)
        return response['candidates'][0]['output']
    except Exception as e:
        logger.error(f"Error fetching hotel details: {traceback.format_exc()}")
        return "Unable to fetch hotel details. Please try again."

# Skyscanner scraping-based tool
def get_flight_details(origin, destination, travel_date, return_date=None):
    """Scrape Skyscanner for flight details."""
    url = f"https://www.skyscanner.net/transport/flights/{origin}/{destination}/{travel_date}/"
    if return_date:
        url += f"{return_date}/"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        # Dummy example: Parse response to extract relevant data
        flights = [
            {"airline": "Air France", "cost": "₹55,000"},
            {"airline": "Lufthansa", "cost": "₹60,000"}
        ]
        return flights
    except Exception as e:
        logger.error(f"Error fetching flight details: {traceback.format_exc()}")
        return "Unable to fetch flight details. Please try again."
