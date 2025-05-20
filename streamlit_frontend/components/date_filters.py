import streamlit as st
from datetime import date

def get_date_filters():
    months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    st.header("Filtrer par période")

    st.subheader("Date de début")
    col1, col2, col3 = st.columns(3)
    with col1:
        start_day = st.selectbox("Jour", list(range(1, 32)))
    with col2:
        start_month = st.selectbox("Mois", months)
    with col3:
        start_year = st.selectbox("Année", list(range(2000, date.today().year + 1)))

    st.subheader("Date de fin (optionnel)")
    col4, col5, col6 = st.columns(3)
    with col4:
        end_day = st.selectbox("Jour (fin)", list(range(1, 32)))
    with col5:
        end_month = st.selectbox("Mois (fin)", months)
    with col6:
        end_year = st.selectbox("Année (fin)", list(range(2000, date.today().year + 1)))

    ignore_max_date = st.checkbox("Ignorer la date de fin")

    start_month_index = months.index(start_month) + 1
    end_month_index = months.index(end_month) + 1 if not ignore_max_date else None

    min_date = f"{start_year}-{start_month_index:02d}-{start_day:02d}"
    max_date = None if ignore_max_date else f"{end_year}-{end_month_index:02d}-{end_day:02d}"

    return min_date, max_date
