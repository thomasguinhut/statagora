import streamlit as st
from service.publication_service import PublicationService
import os

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
            st.subheader(f"{month_year} - Semaine {week}")
            previous_month_year = month_year
            previous_week = week
            st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)

        # Affichage des publications
        col1, col2 = st.columns([1, 4])

        # Dans la première colonne, afficher l'image
        with col1:
            image_path = f"/Users/thomasguinhut/Documents/statagora/data/logos/{row.organisme}.png"
            st.image(image_path)

        # Dans la deuxième colonne, afficher le texte et les informations
        with col2:
            st.markdown(f"**[{row.titre}]({row.lien})** - {row.date} - *{row.collection}*")
            st.write(row.soustitre)

        # Ajoutez un séparateur entre les publications
        st.divider()
