import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set the Google Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
#genai.configure(api_key=api_key)

# Initialize the Gemini model without explicitly passing the API key
model = genai.GenerativeModel("gemini-1.5-flash-002", tools="google_search_retrieval")

# Function to process visa queries
# Agent for Visa
def process_visa_query(user_query):
    try:
        response = model.generate_content(user_query)  # Use Gemini model to generate content
        rc = response.candidates[0]  # Get the first candidate response
        return rc.content.parts[0].text
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"


# Streamlit App UI
st.title("Visa Requirements Assistant")
st.write("Hello! I’m here to assist you with your visa queries. Let’s get started.")

# User input for initial query
user_input = st.text_input("Please describe your visa-related query (e.g., 'I need a visa to travel to France').")

if user_input:
    # Display user input for confirmation
    st.write(f"**Your query:** {user_input}")

    # Ask follow-up questions as free-text inputs
    st.session_state['nationality'] = st.text_input("What is your nationality?")
    st.session_state['destination'] = st.text_input("Which country are you traveling to?")
    st.session_state['travel_purpose'] = st.text_input("What is the purpose of your travel?")
    st.session_state['duration'] = st.text_input("What is the duration of your stay (in weeks)?")

    # Check if all required inputs are provided
    if all([
        st.session_state.get('nationality'),
        st.session_state.get('destination'),
        st.session_state.get('travel_purpose'),
        st.session_state.get('duration')
    ]):
        try:
            # Ensure duration is numeric
            duration = int(st.session_state['duration'])
        except ValueError:
            st.error("Please enter a valid number for the duration of your stay.")
        else:
            # Construct the prompt for the Visa Agent
            visa_prompt = (
                f"What are the visa requirements for a {st.session_state['nationality']} passport holder "
                f"traveling to {st.session_state['destination']} for {duration} weeks "
                f"for {st.session_state['travel_purpose']} purposes?"
            )

            # Display the constructed prompt for debugging
            st.write("**Constructed Visa Query Prompt:**")
            st.text(visa_prompt)

            # Call the Visa Agent
            visa_response = process_visa_query(visa_prompt)

            # Display the response
            st.write("**Visa Information:**")
            st.write(visa_response)