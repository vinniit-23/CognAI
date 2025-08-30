
import streamlit as st

st.title("CognAI")
st.caption("Cognai-From emails to everything, One AI Agent for your work.")

with st.sidebar:
    st.title("CognAI")
    st.caption("Cognai-From emails to everything, One AI Agent for your work.")
    st.write(" History")


prompt = st.chat_input("Enter prompt", key="prompt")

if prompt:
    st.write(f"User has sent the following prompt: {prompt}")



