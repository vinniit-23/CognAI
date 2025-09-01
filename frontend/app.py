
import streamlit as st
import requests
from dotenv import load_dotenv
import os


#API made by fastapi is stored in .env file so setting api key here
load_dotenv()
API_URL =os.getenv("API_URL")


st.title("CognAI")
st.caption("Cognai-From emails to everything, One AI Agent for your work.")

with st.sidebar:
    st.title("CognAI")
    st.caption("Cognai-From emails to everything, One AI Agent for your work.")
    st.chat_input("Search chat")
    st.text("History")

#stored input from user in prompt variable
prompt = st.chat_input("Enter prompt", key="prompt")


if prompt:
    
    st.write(f"User:-  {prompt}")

    try:
        response = requests.post(API_URL, json={"user_prompt": prompt})
        data = response.json()
        st.write(f"CognAI:-  {data["ai_response"]}")
    except Exception as e:
        st.write(f"An error occurred: {e}")



