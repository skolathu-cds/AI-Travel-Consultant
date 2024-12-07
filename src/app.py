import sys
import os

# Dynamically add the 'src' directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import streamlit as st
from src.utils.summary import generate_summary
from src.utils.memory import initialize_memory
from src.agents.visa_agent import process_query as visa_query
from src.agents.air_agent import process_query as air_query
from src.agents.hotel_agent import process_query as hotel_query
from src.agents.policy_agent import process_query as policy_query
from src.agents.city_airport_agent import process_query as city_airport_query
from src.utils.prompt_utils import reengineer_prompt  # Import the prompt utility
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Initialize memory
memory = initialize_memory()

# Main Chat Section
st.title("Welcome to Smart Travel Consultant")
st.write("Hello! I’m your AI travel consultant here to assist you with your travel plans.")

# Step 1: User Input for Travel Query (e.g., "I need to travel to Tokyo")
user_input = st.text_input("How can I assist you with your travel today?")

if user_input:
    # Step 2: Context Understanding by LLM
    llm = OpenAI(temperature=0.7)  # Using OpenAI to process the input

    # Example prompt to understand the context (e.g., destination and travel intent)
    prompt = f"User said: '{user_input}'. What is the user's travel intent? What additional details should I ask to assist with travel planning?"
    context = llm(prompt)  # Get the response from OpenAI

    st.write(f"**STC:** Based on your input, here's what I understand: {context}")

    # Step 3: Follow-up Questions Based on Detected Context (Travel destination)
    if "travel" in user_input.lower():  # Detect if it's a travel-related query
        # Ask follow-up questions for the user's trip (purpose, date, duration, nationality)
        st.session_state['purpose'] = st.selectbox("What is the purpose of your visit?", ["Business", "Leisure", "Other"])
        st.session_state['travel_date'] = st.date_input("When are you planning to travel?")
        st.session_state['duration'] = st.number_input("How long will you be staying?", min_value=1, max_value=90)
        st.session_state['nationality'] = st.text_input("What is your passport issuing country?")
    
    # Step 4: Visa Agent Invocation (if all details are provided)
    if all([st.session_state.get('purpose'), st.session_state.get('travel_date'), st.session_state.get('duration'), st.session_state.get('nationality')]):
        st.write(f"Thanks for providing the details. Now I’ll check the visa requirements for you.")
        
        # Construct the visa query
        visa_prompt = f"What is the visa requirement for a {st.session_state['nationality']} passport holder traveling to {user_input.split('to')[-1].strip()} for {st.session_state['duration']} weeks?"
        visa_response = visa_query(visa_prompt)  # Invokes Visa Agent with the query
        st.write(f"**Visa Information**: {visa_response}")
        
        # Step 5: Ask for More Information on Flights or Hotels
        user_needs = st.radio("Would you like to know more about hotels or flights?", ["Hotels", "Flights", "No, thanks"])
        
        if user_needs == "Hotels":
            st.session_state['pincode'] = st.text_input("Can you provide your destination pin code?")
            if st.session_state.get('pincode'):
                hotel_prompt = f"List 5-star hotels near {st.session_state['pincode']} for the dates from {st.session_state['travel_date']} for {st.session_state['duration']} weeks."
                hotel_response = hotel_query(hotel_prompt)
                st.write(f"**Hotel Options**: {hotel_response}")
        
        if user_needs == "Flights":
            air_prompt = f"Provide flight options from your origin city to {user_input.split('to')[-1].strip()} for the travel dates from {st.session_state['travel_date']} for {st.session_state['duration']} weeks."
            air_response = air_query(air_prompt)
            st.write(f"**Flight Options**: {air_response}")

        # Final summary and download option
        st.write("Here’s a summary of your travel details:")
        st.write(f"Visa: {visa_response}")
        st.write(f"Hotel Options: {hotel_response if user_needs == 'Hotels' else 'Not requested'}")
        st.write(f"Flight Options: {air_response if user_needs == 'Flights' else 'Not requested'}")

        # Final summary download option
        st.download_button(
            label="Download Travel Summary",
            data=generate_summary(memory),  # Generates and downloads the summary
            file_name="travel_summary.pdf",
            mime="application/pdf"
        )