import streamlit as st
from service.publication_service import PublicationService
import os

st.title("Statagora")

# Initialiser les variables
previous_month_year = ""
previous_week = -1

publications = PublicationService().tout_afficher()
if publications:
    for row in publications:
        # Obtenir le mois/année et la semaine de la date de publication
        month_year, week = row.get_month_year_and_week()

        # Afficher le titre si le mois/année ou la semaine a changé
        if month_year and week and (month_year != previous_month_year or week != previous_week):
            st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)
            st.subheader(f"{month_year} - S{week}")
            previous_month_year = month_year
            previous_week = week

        st.markdown(
            f"- {row.organisme.upper()} - {row.date} - *{row.collection}*  \n"
            f"**[{row.titre}]({row.lien})**",
            unsafe_allow_html=True,
        )
        if row.soustitre:
            with st.expander("Afficher le résumé"):
                st.write(row.soustitre)
        st.write("")
