import streamlit as st
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

def login_page():
    st.title("Connexion")

    # Champs de connexion
    username = st.text_input("User Agent")
    password = st.text_input("Token API", type="password")

    # Bouton de connexion
    if st.button("Se connecter"):
        # Récupérer les valeurs depuis le fichier .env et supprimer les espaces inutiles
        stored_user_agent = os.getenv("USER_AGENT", "").strip()
        stored_token_api = os.getenv("TOKEN_API", "").strip()

        # Supprimer les espaces inutiles dans les entrées utilisateur
        username = username.strip()
        password = password.strip()

        # Vérifier si les champs correspondent aux valeurs stockées
        if username == stored_user_agent and password == stored_token_api:
            st.session_state["authenticated"] = True  # Marquer l'utilisateur comme connecté
            st.success("Connexion réussie ! Redirection vers le tableau de bord...")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
            st.write(f"Stored User Agent: {stored_user_agent}")
            st.write(f"Stored Token API: {stored_token_api}")
            st.write(f"Input User Agent: {username}")
            st.write(f"Input Token API: {password}")

    # Bouton pour accéder à la page d'inscription
    if st.button("Pas encore inscrit ? Cliquez ici pour vous inscrire."):
        st.session_state["show_registration"] = True
