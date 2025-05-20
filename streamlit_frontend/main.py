import streamlit as st
from pages.login import login_page
from pages.dashboard import dashboard_page
from pages.register import register_page

# Initialiser l'état de session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "show_registration" not in st.session_state:
    st.session_state["show_registration"] = False

# Afficher la page appropriée
if st.session_state["authenticated"]:
    dashboard_page()
elif st.session_state["show_registration"]:
    register_page()
else:
    login_page()
