import logging
import streamlit as st
from streamlit_gsheets import GSheetsConnection


from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class PublicationDao:

    @log
    def creer(self, publication):
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet = conn.open("statagora")
        worksheet = sheet.worksheet("base")
        worksheet.append_row(
            [
                publication.titre,
                publication.date_obj,
                publication.lien,
                publication.organisme,
                publication.sousitre,
                publication.organisation,
            ]
        )

    def tout_afficher(self):
        # Connexion à la base de données PostgreSQL
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        return df

    def afficher_date_la_plus_récente(self, organisme):
        conn = st.connection("postgresql", type="sql")
        query = f"""
        SELECT MAX(date_publication) AS date_la_plus_récente
        FROM statagora.publication
        WHERE organisme_publication = '{organisme}'
        """
        df = conn.query(query)
        return df.iloc[0]["date_la_plus_récente"] if not df.empty else None

    def nom_explicite_organisme(self, id_organisme):
        conn = st.connection("postgresql", type="sql")
        query = f"""
        SELECT nom_explicite_organisme 
        FROM statagora.organisme
        WHERE nom_organisme = '{id_organisme}'
        """
        df = conn.query(query)
        return df.iloc[0]["nom_explicite_organisme"] if not df.empty else None


if __name__ == "__main__":
    dao = PublicationDao()
    print(dao.nom_explicite_organisme("dares"))
