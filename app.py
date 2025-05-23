import streamlit as st
import google.generativeai as genai
# import os # You don't need 'os' or 'dotenv' for secrets on Streamlit Cloud
# from dotenv import load_dotenv # You don't need 'dotenv' for secrets on Streamlit Cloud
# load_dotenv() ## loading all the environment variables (Not needed for Streamlit Cloud secrets)

# Configure API key using Streamlit's secrets management
# This is the correct way to access secrets in Streamlit Cloud
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

## Function to load Gemini Flash model and get responses
# Using 'models/gemini-1.5-flash' as per your last successful model
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# --- Streamlit UI Enhancements ---

st.set_page_config(
    page_title="Intelligent Rohit's Chatbot",
    page_icon="✨", # A nice emoji icon
    layout="centered", # Can be "wide" or "centered"
    initial_sidebar_state="auto" # Can be "auto", "expanded", or "collapsed"
)

# Custom CSS for a dark theme
st.markdown("""
<style>
    /* Overall app background - Black */
    .stApp {
        background-color: #1a1a1a; /* Very dark gray/off-black */
        color: #ffffff; /* White text for general content */
    }

    /* Targeting the main content block for padding */
    .st-emotion-cache-nahz7x {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Title and main headers - White */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }

    /* General text within st.write - White */
    .stMarkdown {
        color: #ffffff;
    }

    /* Style for the chat messages */
    /* User message container - Darker gray for contrast */
    .st-emotion-cache-1c7y2qn {
        background-color: #333333; /* Dark gray */
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3); /* Darker shadow */
    }
    /* Bot message container - Slightly lighter gray for bot */
    .st-emotion-cache-1v0m0h5 {
        background-color: #2b2b2b; /* Slightly lighter than app background */
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3); /* Darker shadow */
    }

    /* Specific styling for the roles inside messages - White */
    .st-chat-message-user .stMarkdown {
        color: #ffffff; /* White text for user messages */
    }
    .st-chat-message-ai .stMarkdown {
        color: #e0e0e0; /* Off-white for bot messages */
    }

    /* Spinner text color - White */
    .stSpinner > div > div {
        color: #ffffff;
    }

    /* Buttons - Darker green for contrast on dark background */
    .stButton>button {
        background-color: #2e7d32; /* Darker green */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #1b5e20; /* Even darker green on hover */
    }

    /* Text Input box - Dark background, white text */
    .stTextInput>div>div>input {
        background-color: #222222; /* Dark gray input field */
        color: #ffffff; /* White text in input field */
        border-radius: 8px;
        border: 1px solid #444444; /* Slightly lighter border for visibility */
        padding: 10px;
    }
    /* Text input label - White */
    .stTextInput>label {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌟 Intelligent Rohit's Chatbot")
st.markdown("---")
st.write("Hello! I'm your AI assistant, powered by Google's Gemini Flash model. Ask me anything!")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize Gemini chat model only once
# This ensures the conversation context is maintained across interactions
if 'gemini_chat' not in st.session_state:
    st.session_state['gemini_chat'] = model.start_chat(history=[])

# Function to get Gemini response using the session-persisted chat object
def get_gemini_response(question):
    response = st.session_state['gemini_chat'].send_message(question, stream=True)
    return response

# Display chat messages from history on app rerun
for role, text in st.session_state['chat_history']:
    with st.chat_message(role):
        st.markdown(text)

# Input box and submit button at the bottom
col1, col2 = st.columns([4, 1]) # Adjust column width for input and button

with col1:
    user_query = st.text_input("Say something...", key="user_input_text")

with col2:
    submit_button = st.button("Send", key="send_button")


# Process user input when 'Send' button is clicked OR Enter is pressed in text_input
if submit_button and user_query:
    # Add user query to chat history immediately
    st.session_state['chat_history'].append(("user", user_query))

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Get and display bot response
    with st.chat_message("assistant"): # Use "assistant" for bot messages
        with st.spinner("Thinking..."): # Show a spinner while waiting for response
            full_response = ""
            response_chunks = get_gemini_response(user_query)
            
            response_container = st.empty() # Placeholder for streaming text
            for chunk in response_chunks:
                full_response += chunk.text
                response_container.markdown(full_response + "▌") # Add blinking cursor for streaming
            response_container.markdown(full_response) # Display final response without cursor

            # Add bot response to chat history
            st.session_state['chat_history'].append(("assistant", full_response))
    
    # Clear the input box after submission
    st.rerun() # Rerun to clear the input box and update chat

# Add a "Clear Chat" button
st.markdown("---") # Separator
if st.button("Clear Chat History", key="clear_chat_button"):
    st.session_state['chat_history'] = []
    # Re-initialize the chat object to clear its internal history too
    st.session_state['gemini_chat'] = model.start_chat(history=[])
    st.rerun() # Rerun the app to clear display and history
