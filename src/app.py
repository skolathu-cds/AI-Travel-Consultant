import streamlit as st
from all_agents import (
    process_visa_query,
    process_air_query,
    process_hotel_query,
    process_city_airport_query,
    reengineer_prompt,
    generate_summary
)
from utils.memory import initialize_memory
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Initialize memory
memory = initialize_memory()

# Main Chat Section
st.title("Welcome to Smart Travel Consultant")
st.write("Hello! I’m your AI travel consultant here to assist you with your travel plans.")

# Step 1: User Input for Travel Query (e.g., "I need to travel to Finland")
user_input = st.text_input("How can I assist you with your travel today?")

if user_input:
    # Step 2: Context Understanding by LLM (Optional: Can be bypassed if not required)
    llm = OpenAI(temperature=0.7)  # Using OpenAI to process the input

    # Example prompt to understand the context (e.g., destination and travel intent)
    prompt = f"User said: '{user_input}'. What additional details should I ask to assist with travel planning?"
    context = llm(prompt)  # Get the response from OpenAI

    # Manually trigger the follow-up questions instead of asking internally
    st.write(f"**STC:** Based on your input, I'll need some more details to assist you with your travel planning.")

    # Ask follow-up questions in a structured manner
    st.session_state['purpose'] = st.selectbox("What is the purpose of your visit?", ["Business", "Leisure", "Other"])
    st.session_state['travel_date'] = st.date_input("When are you planning to travel?")
    st.session_state['duration'] = st.number_input("How long will you be staying?", min_value=1, max_value=90)
    st.session_state['nationality'] = st.text_input("What is your passport issuing country?")
    
    # Step 4: Visa Agent Invocation (if all details are provided)
    if all([st.session_state.get('purpose'), st.session_state.get('travel_date'), st.session_state.get('duration'), st.session_state.get('nationality')]):
        st.write(f"Thanks for providing the details. Now I’ll check the visa requirements for you.")
        
        # Construct the visa query
        visa_prompt = f"What is the visa requirement for a {st.session_state['nationality']} passport holder traveling to {user_input.split('to')[-1].strip()} for {st.session_state['duration']} weeks?"
        visa_response = process_visa_query(visa_prompt)  # Invokes Visa Agent with the query
        st.write(f"**Visa Information**: {visa_response}")
        
        # Step 5: Ask for More Information on Flights or Hotels
        user_needs = st.radio("Would you like to know more about hotels or flights?", ["Hotels", "Flights", "No, thanks"])
        
        if user_needs == "Hotels":
            st.session_state['pincode'] = st.text_input("Can you provide your destination pin code?")
            if st.session_state.get('pincode'):
                hotel_prompt = f"List 5-star hotels near {st.session_state['pincode']} for the dates from {st.session_state['travel_date']} for {st.session_state['duration']} weeks."
                hotel_response = process_hotel_query(hotel_prompt)
                st.write(f"**Hotel Options**: {hotel_response}")
        
        if user_needs == "Flights":
            air_prompt = f"Provide flight options from your origin city to {user_input.split('to')[-1].strip()} for the travel dates from {st.session_state['travel_date']} for {st.session_state['duration']} weeks."
            air_response = process_air_query(air_prompt)
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