import streamlit as st
import os

def update_env_variable(key, value, env_file=".env"):
    """
    Met à jour ou ajoute une variable d'environnement dans le fichier .env.
    """
    try:
        # Lire le contenu existant du fichier .env
        if os.path.exists(env_file):
            with open(env_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []

        # Vérifier si la clé existe déjà
        updated = False
        with open(env_file, "w") as file:
            for line in lines:
                if line.startswith(f"{key}="):
                    file.write(f'{key}="{value}"\n')
                    updated = True
                else:
                    file.write(line)
            # Ajouter la clé si elle n'existe pas
            if not updated:
                file.write(f'{key}="{value}"\n')
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la mise à jour du fichier .env : {e}")

def register_page():
    st.title("Inscription")

    # Champs d'inscription
    # username = st.text_input("Nom d'utilisateur")
    # email = st.text_input("Adresse email")
    # password = st.text_input("Mot de passe", type="password")
    # confirm_password = st.text_input("Confirmer le mot de passe", type="password")
    user_agent = st.text_input("User Agent")
    token_api = st.text_input("Token API", type="password")

    # Bouton d'inscription
    if st.button("S'inscrire"):
        # Vérifier que les mots de passe correspondent
        # if password != confirm_password:
        #     st.error("Les mots de passe ne correspondent pas.")
        # # Vérifier que tous les champs sont remplis
        # elif not username or not email or not password or not user_agent or not token_api:
        if not user_agent or not token_api:
            st.error("Tous les champs sont obligatoires.")
        else:
            try:
                # Enregistrer les informations dans le fichier .env
                update_env_variable("USER_AGENT", f"{user_agent}")
                update_env_variable("TOKEN_API", f"{token_api}")

                # Simuler l'inscription (vous pouvez ajouter une logique pour enregistrer les données)
                st.success("Inscription réussie ! Vous pouvez maintenant vous connecter.")
                st.session_state["show_registration"] = False
            except RuntimeError as e:
                st.error(f"Erreur lors de l'inscription : {e}")
