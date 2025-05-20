import streamlit as st
from components.sidebar import render_sidebar
from components.date_filters import get_date_filters
from components.gif_loader import get_random_gif
from services.get_recurent_bills import get_all_fixed_costs, clean_df, validate_date
import pandas as pd

def dashboard_page():
    st.title("Cybncom Facturation")

    # Barre latérale
    person_id, api_url, api_key = render_sidebar()

    # Filtres de dates
    min_date, max_date = get_date_filters()

    # Bouton pour valider les dates et récupérer les données
    if st.button("Extraire les factures"):
        if not min_date:
            st.error("La date de début est obligatoire.")
        else:
            try:
                min_date = validate_date(min_date)
                if max_date:
                    max_date = validate_date(max_date)
            except ValueError as e:
                st.error(str(e))
            else:
                gif_placeholder = st.empty()
                random_gif = get_random_gif()
                if random_gif:
                    gif_placeholder.image(random_gif, use_column_width=True)

                with st.spinner("Chargement des données..."):
                    try:
                        all_fixed_costs = get_all_fixed_costs(person_id, min_date, max_date)

                        if isinstance(all_fixed_costs, pd.DataFrame) and not all_fixed_costs.empty:
                            cleaned_data = clean_df(all_fixed_costs)
                            st.success("Les données ont été récupérées et nettoyées avec succès !")
                            st.dataframe(cleaned_data)
                            st.download_button(
                                label="Télécharger le fichier CSV",
                                data=cleaned_data.to_csv(index=False).encode('utf-8'),
                                file_name="fixed_costs.csv",
                                mime="text/csv"
                            )
                        else:
                            st.warning("Aucun coût fixe trouvé pour la période sélectionnée.")
                    except Exception as e:
                        st.error(f"Erreur lors de la récupération des données : {e}")
                    finally:
                        gif_placeholder.empty()
