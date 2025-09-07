import streamlit as st
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("CognAI — Connect Gmail via Descope")
user_id = st.text_input("Descope User ID", key="user_id")

if st.button("Start Login & Connect"):
    st.write("Opening Descope login...")
    st.write("[Click here to proceed →](http://127.0.0.1:5500/backend/template/auth.html)", unsafe_allow_html=True)

if st.button("Connect Gmail"):
    if not user_id:
        st.error("Enter your Descope User ID")
    else:
        resp = requests.post(f"{API_URL}/start_connect", json={"userId": user_id}, timeout=15)
        if resp.status_code == 200:
            url = resp.json().get("url")
            st.write("Open this link to grant Gmail permissions:")
            st.write(f"[Connect via Google]({url})", unsafe_allow_html=True)
        else:
            st.error(resp.json())

if st.button("Fetch Emails"):
    if not user_id:
        st.error("Enter your Descope User ID")
    else:
        resp = requests.get(f"{API_URL}/emails", params={"userId": user_id}, timeout=15)
        if resp.status_code == 200:
            st.json(resp.json())
        else:
            st.error(resp.json())
