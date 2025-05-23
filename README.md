# 🌟 Intelligent Rohit's Chatbot

An interactive chatbot web app built with **Streamlit** and powered by **Google's Gemini 1.5 Flash model**. This assistant is styled with a sleek dark theme and supports streaming chat responses.

## 🚀 Features

- 🔮 Uses `gemini-1.5-flash` from Google Generative AI
- 💬 Persistent chat history using `st.session_state`
- 🌙 Custom dark theme for an elegant UI
- ⚡ Fast, streaming responses
- 🧹 "Clear Chat" functionality
- ✅ Designed to run on **Streamlit Cloud** with secure secrets management

## 🛠️ Setup Instructions

1. **Clone this repo** (or copy `app.py` content).
2. **Add your API key** to Streamlit Cloud secrets:
   - Go to **Settings → Secrets** and add:
     ```toml
     GOOGLE_API_KEY = "your-google-api-key"
     ```
3. **Deploy to Streamlit Cloud** or run locally:
   ```bash
   streamlit run app.py 

📌 Requirements

Python 3.8+
Streamlit
google-generativeai


Made with ❤️ by Rohit.
