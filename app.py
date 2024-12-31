import sys
import os

# Ajouter le répertoire parent de src au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from src.service.publication_service import PublicationService
from datetime import datetime, timedelta

# Configuration du nom et du logo + centrage de la page sur l'écran
st.set_page_config(page_title="Statagora", page_icon="📊", layout="centered")

st.title("📊 Statagora")

st.write("")
text_search = st.text_input("", value="")
if text_search:
    filtre = PublicationService().rechercher_publications(text_search, 10)
else:
    text_search = None

# Ajouter du CSS personnalisé
st.markdown(
    """
    <style>
    .publication-title a:hover {
        color: #FF4C4B !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Fonction pour mettre en cache les publications pendant une journée
@st.cache_data(ttl=86400)  # 86400 secondes = 1 jour
def get_publications():
    return PublicationService().afficher_publications()


# Initialiser les variables
previous_month_year = ""
previous_week = -1

publications = get_publications()
if text_search is not None:
    publication_filtrees = []
    for publication in publications:
        if publication.titre_publication in filtre:
            publication_filtrees.append(publication)
    publication_filtrees.sort(key=lambda pub: filtre.index(pub.titre_publication))
    for publication in publication_filtrees:
        date_str = publication.date_publication
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")

        st.markdown(
            f"- <strong class='publication-title'><a href='{publication.lien_publication}' style='color: white;'>{publication.titre_publication}</a></strong>  \n"
            f"<span style='opacity: 0.7;'>{publication.nom_officiel_organisme} - {formatted_date} - <em>{publication.collection_publication}</em></span>",
            unsafe_allow_html=True,
        )
        if publication.soustitre_publication:
            with st.expander("Afficher le résumé"):
                st.write(publication.soustitre_publication)
        st.write("")
else:
    for publication in publications:
        # Obtenir le mois/année et la semaine de la date de publication
        month_year, week = publication.get_month_year_and_week()

        # Afficher le titre si le mois/année ou la semaine a changé
        if month_year != previous_month_year or week != previous_week:
            st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)
            st.subheader(f"📆 {month_year} - S{week}")
            st.write("")
            previous_month_year = month_year
            previous_week = week

        date_str = publication.date_publication
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")

        st.markdown(
            f"- <strong class='publication-title'><a href='{publication.lien_publication}' style='color: white;'>{publication.titre_publication}</a></strong>  \n"
            f"<span style='opacity: 0.7;'>{publication.nom_officiel_organisme} - {formatted_date} - <em>{publication.collection_publication}</em></span>",
            unsafe_allow_html=True,
        )
        if publication.soustitre_publication:
            with st.expander("Afficher le résumé"):
                st.write(publication.soustitre_publication)
        st.write("")
