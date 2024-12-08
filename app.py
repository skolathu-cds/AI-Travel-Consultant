import streamlit as st
from travel_service_agent import generate_response

# Streamlit application layout
st.title("AI Travel Consultant")
st.markdown("""
    Welcome to the AI Travel Consultant! This tool helps you with travel-related queries, 
    such as visa requirements, flight options, hotel recommendations, and more.
""")

# User input field for travel queries
user_query = st.text_input("Enter your travel query:")

# Button to submit query
if st.button("Get Response"):
    if user_query:
        # Call the function to get the response based on the user query
        response = generate_response(user_query)
        
        # Display the response to the user
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please enter a query to get started.")

