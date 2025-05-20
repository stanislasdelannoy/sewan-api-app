import streamlit as st
import os

def render_sidebar():
    st.sidebar.header("Paramètres")
    person_id = st.sidebar.text_input("ID Client", value=int(os.getenv("PERSON_ID", 0)))
    api_url = st.sidebar.text_input("URL API", value=os.getenv("API_URL"))
    api_key = st.sidebar.text_input("Token API", value=os.getenv("TOKEN_API"), type="password")
    return person_id, api_url, api_key
