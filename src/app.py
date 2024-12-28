import streamlit as st
from service.publication_service import PublicationService
import os
from datetime import datetime, date


st.title("📊 Statagora")

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
            st.subheader(f"📆 {month_year} - S{week}")
            st.write("")
            previous_month_year = month_year
            previous_week = week

        st.markdown(
            f"- <strong><a href='{row.lien}' style='color: white;'>{row.titre}</a></strong>  \n"
            f"<span style='opacity: 0.7;'>{PublicationService().nom_explicite_organisme(row.organisme)} - {row.date.strftime('%d/%m/%Y')} - <em>{row.collection}</em></span>",
            unsafe_allow_html=True,
        )
        if row.soustitre:
            with st.expander("Afficher le résumé"):
                st.write(row.soustitre)
        st.write("")
