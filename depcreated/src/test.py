import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API key (for OpenAI interaction)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the Google Gemini API key (for real-time information)
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)  # Initialize Google Gemini

# Initialize session state for conversation
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context' not in st.session_state:
    st.session_state['context'] = {}

# Function to query OpenAI for chat-based interaction
def ask_openai(question, messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5-turbo for the conversation flow
            messages=messages + [{"role": "user", "content": question}],
            max_tokens=150,
            temperature=0.7  # Adjust the creativity of the response
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to process visa query with Google Gemini
def process_visa_query(user_query):
    try:
        # Generate content using the Gemini model
        response = genai.generate_text(
            model="gemini-1.5-flash-002",  # Specify the model version
            prompt=user_query,
            tools=["google_search_retrieval"]  # Enable grounding via Google Search
        )
        return response['candidates'][0]['output']
    except Exception as e:
        return f"Error: Unable to fetch response. {str(e)}"

# Streamlit App UI
st.title("Visa Requirements Assistant")

# Display conversation history (messages between user and assistant)
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**You**: {message['content']}")
    else:
        st.write(f"**Assistant**: {message['content']}")

# Start interaction with user if no messages yet
if len(st.session_state['messages']) == 0:
    assistant_message = "Hello! How can I assist you with your travel plans today?"
    st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})

# Single input box at the bottom for user to type their response
user_input = st.text_input("Your response here:")

if user_input:
    # Add user input to conversation history
    st.session_state['messages'].append({'role': 'user', 'content': user_input})

    # Check if the user is asking about a visa and if enough details have been provided
    if 'visa' in user_input.lower():
        if 'destination' not in st.session_state['context']:
            # Ask for the destination country
            assistant_message = ask_openai(f"Great! What country are you planning to travel to?", st.session_state['messages'])
            st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})
            st.session_state['context']['destination'] = user_input  # Store destination
        elif 'purpose' not in st.session_state['context']:
            # Ask for the purpose of the travel
            assistant_message = ask_openai(f"Got it! What is the purpose of your travel (e.g., tourism, business, study)?", st.session_state['messages'])
            st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})
            st.session_state['context']['purpose'] = user_input  # Store purpose
        elif 'duration' not in st.session_state['context']:
            # Ask for the duration of the stay
            assistant_message = ask_openai(f"Thanks! How long will you be staying (in weeks)?", st.session_state['messages'])
            st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})
            st.session_state['context']['duration'] = user_input  # Store duration
        elif 'nationality' not in st.session_state['context']:
            # Ask for nationality
            assistant_message = ask_openai(f"Thanks! What is your nationality?", st.session_state['messages'])
            st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})
            st.session_state['context']['nationality'] = user_input  # Store nationality

        # If all required info is gathered, construct visa query
        if all(key in st.session_state['context'] for key in ['destination', 'purpose', 'duration', 'nationality']):
            # Construct the visa query
            visa_prompt = f"What are the visa requirements for a {st.session_state['context']['nationality']} passport holder traveling to {st.session_state['context']['destination']} for {st.session_state['context']['duration']} weeks for {st.session_state['context']['purpose']} purposes?"
            visa_response = process_visa_query(visa_prompt)

            st.session_state['messages'].append({'role': 'assistant', 'content': visa_response})

            # End the conversation or reset as needed
            st.session_state['messages'].append({'role': 'assistant', 'content': "I’ve provided the visa information. Do you have any other questions?"})

    # Handle any other responses or user needs
    else:
        assistant_message = ask_openai(f"Thanks! How can I assist you further?", st.session_state['messages'])
        st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message})

# The input box stays at the bottom as the only one