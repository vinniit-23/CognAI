
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


st.title("CognAI")
st.caption("Cognai-From emails to everything, One AI Agent for your work.")

with st.sidebar:
    st.title("CognAI")
    st.caption("Cognai-From emails to everything, One AI Agent for your work.")
    st.chat_input("Search chat")
    st.text("History")

#stored input from user in prompt variable
prompt = st.chat_input("Enter prompt", key="prompt")

model= genai.GenerativeModel('gemini-1.5-flash')

if prompt:
    
    st.write(f"User:-  {prompt}")

    try:
      response =model.generate_content(prompt)
      st.write(f"gemini:-  {response.text}")
    except Exception as e:
        st.write(f"An error occurred: {e}")



