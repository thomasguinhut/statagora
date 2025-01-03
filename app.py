import sys
import os

import streamlit as st
from datetime import datetime
from src.service.publication_service import PublicationService
from src.business_objet.publication import Publication
from src.business_objet.organisme import Organisme
from src.dao.db_connection import DBConnection
from src.dao.reset_database import ResetDatabase
import pandas as pd
import logging

from src.utils.log_decorator import log

# Configuration du nom et du logo + centrage de la page sur l'écran
st.set_page_config(page_title="Statagora", page_icon="📊", layout="centered")

# Ajouter le répertoire parent de src au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


@log
@st.cache_data(ttl=3600)
def get_df(ignore_cache=False):
    return DBConnection().afficher_df()


@log
def get_publication_service(df):
    return PublicationService(df)


@log
def display_publication(publication):
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


@log
def display_mois_semaine(previous_month_year, previous_week, publication):
    month_year, week = publication.get_month_year_and_week()
    if month_year != previous_month_year or week != previous_week:
        st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)
        st.subheader(f"📆 {month_year} - S{week}")
        st.write("")
        return month_year, week
    return previous_month_year, previous_week


df = get_df()
publication_service = get_publication_service(df)

if ResetDatabase().doit_reset():
    ResetDatabase().reset_publications(df, True)
    ResetDatabase().enregistrer_date_derniere_ouverture()
    st.cache_data.clear()
    st.rerun(scope="app")

st.markdown(
    """
    <style>
    .title {
        text-align: left;
        color: white;
        font-size: 6em; /* Ajustez cette valeur pour agrandir ou réduire la taille */
    }
    .title a {
        color: white;
        text-decoration: none;
    }
    .reset-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .search-bar {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    <h1 class='title'>
        <a href='https://statagora.streamlit.app/'>📊 Statagora</a>
    </h1>
    """,
    unsafe_allow_html=True,
)

# Ajouter un bouton pour réinitialiser les publications
if st.button("Réinitialiser les publications"):
    try:
        ResetDatabase().reset_publications(df, True)
        ResetDatabase().enregistrer_date_derniere_ouverture()
        st.cache_data.clear()
        st.rerun(scope="app")
    except OSError as e:
        st.error(f"Erreur d'entrée/sortie lors de la réinitialisation des publications : {e}")

st.markdown("<div class='search-bar'>", unsafe_allow_html=True)
col1, col2 = st.columns([7, 3])
with col1:
    text_search = st.text_input("Recherche de publications", value="", label_visibility="hidden")
with col2:
    organisme = st.selectbox(
        label="Organisme",
        options=["Tous organismes", "Dares", "Insee", "SSM-SI"],
        index=0,
        label_visibility="hidden",
    )
    if organisme and organisme != "Tous organismes":
        id_organisme = Organisme(nom_officiel_organisme=organisme).get_id_organisme(organisme)
    else:
        id_organisme = None
st.markdown("</div>", unsafe_allow_html=True)

# Filtrage des publications
if text_search and organisme and organisme != "Tous organismes":
    filtre = publication_service.rechercher_publications(text_search, 10, id_organisme)
elif text_search:
    filtre = publication_service.rechercher_publications(text_search, 10)
elif organisme and organisme != "Tous organismes":
    filtre = publication_service.afficher_publications_organisme(id_organisme)
else:
    filtre = None

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

# Initialiser les publications
publications = publication_service.afficher_publications()

# Afficher les publications en fonction du filtre
if filtre is not None:
    if text_search:
        publication_filtrees = [pub for pub in publications if pub.titre_publication in filtre]
        publication_filtrees.sort(key=lambda pub: filtre.index(pub.titre_publication))
        for publication in publication_filtrees:
            display_publication(publication)
    else:
        publication_filtrees = [pub for pub in publications if pub.titre_publication in filtre]
        previous_month_year = ""
        previous_week = -1
        for publication in publication_filtrees:
            previous_month_year, previous_week = display_mois_semaine(
                previous_month_year, previous_week, publication
            )
            display_publication(publication)
else:
    previous_month_year = ""
    previous_week = -1
    for publication in publications:
        previous_month_year, previous_week = display_mois_semaine(
            previous_month_year, previous_week, publication
        )
        display_publication(publication)
