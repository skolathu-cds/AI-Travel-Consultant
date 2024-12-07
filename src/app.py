import streamlit as st
from src.utils.summary import generate_summary
from src.utils.memory import initialize_memory
from src.agents.visa_agent import process_query as visa_query
from src.agents.air_agent import process_query as air_query
from src.agents.hotel_agent import process_query as hotel_query
from src.agents.policy_agent import process_query as policy_query
from src.agents.city_airport_agent import process_query as city_airport_query
from src.utils.prompt_utils import reengineer_prompt  # Import the new prompt utility

# Initialize memory
memory = initialize_memory()

# Sidebar Navigation
st.sidebar.title("Smart Travel Consultant")
st.sidebar.subheader("Navigation")
option = st.sidebar.radio("Go to", ["Chat", "About the Tool", "Disclaimer"])

# About the Tool Section
if option == "About the Tool":
    st.title("About Smart Travel Consultant")
    st.write("""
    The Smart Travel Consultant is your AI-powered assistant to plan travel effectively. 
    It provides information on visas, flights, hotels, and travel policies using AI technologies like LangChain and RAG.
    """)

# Disclaimer Section
elif option == "Disclaimer":
    st.title("Disclaimer")
    st.write("""
    This tool provides travel assistance based on publicly available information and internal travel policy documents. 
    Please verify all recommendations independently.
    """)

# Main Chat Section
else:
    st.title("Welcome to Smart Travel Consultant")
    st.write("Hello! I’m your AI travel consultant here to assist you with your travel plans.")

    # Chat Input
    user_input = st.text_input("Type your question here:", key="user_input")

    # Example context dictionary (to be dynamically updated during the conversation)
    context = {
        "nationality": "India",           # Example data, to be dynamically updated
        "destination": "France",          # Example data
        "departure_city": "Bangalore",    # Example data
        "policy_details": "Eligible for 3-star hotels, economy class flights, and $50 per diem.",  # Example data
        "policy_text": "Company travel policy content goes here."  # Example data
    }

    if user_input:
        # Reengineer the prompt using user query and context
        reengineered_prompt = reengineer_prompt(user_input, context)

        # Route the reengineered prompt to the appropriate agent
        if "visa" in user_input.lower():
            response = visa_query(reengineered_prompt)
        elif "flight" in user_input.lower():
            response = air_query(reengineered_prompt)
        elif "hotel" in user_input.lower():
            response = hotel_query(reengineered_prompt)
        elif "policy" in user_input.lower():
            response = policy_query(reengineered_prompt)
        elif "city" in user_input.lower() or "airport" in user_input.lower():
            response = city_airport_query(reengineered_prompt)
        else:
            response = "I'm sorry, I couldn't understand your query. Could you rephrase it?"

        # Display response
        st.write(f"**STC:** {response}")
        
        # Save to memory
        memory.store_response(user_input, response)

    # Final Summary Download
    if st.button("Download Travel Summary"):
        summary = generate_summary(memory)
        st.download_button(
            label="Download Summary",
            data=summary,
            file_name="final_summary.pdf",
            mime="application/pdf"
        )