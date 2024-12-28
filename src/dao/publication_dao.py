import logging
import streamlit as st


from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class PublicationDao:

    @log
    def creer(self, publication) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO publication(titre_publication,
                                                date_publication, lien_publication,
                                                organisme_publication, soustitre_publication,
                                                collection_publication) VALUES
                        (%(titre_publication)s, %(date_publication)s,
                        %(lien_publication)s, %(organisme_publication)s,
                        %(soustitre_publication)s, %(collection_publication)s)
                            RETURNING titre_publication;
                        """,
                        {
                            "titre_publication": publication.titre,
                            "date_publication": publication.date,
                            "lien_publication": publication.lien,
                            "organisme_publication": publication.organisme,
                            "soustitre_publication": publication.soustitre,
                            "collection_publication": publication.collection,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise
        created = False
        if res:
            created = True
        return created

    def tout_afficher(self):
        # Connexion à la base de données PostgreSQL
        conn = st.connection("postgresql", type="sql")
        # Requête SQL pour récupérer les publications et les logos
        query = """
        SELECT *
            FROM statagora.publication p
            LEFT JOIN statagora.organisme o ON p.organisme_publication = o.nom_organisme
        """
        # Exécution de la requête sans cache
        df = conn.query(query)
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
