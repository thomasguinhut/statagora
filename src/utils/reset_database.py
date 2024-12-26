import os
import dotenv
import logging

from log_decorator import log
from singleton import Singleton
from dao.db_connection import DBConnection
from client.dares_client import DaresClient
from service.publication_service import PublicationService
from service.organisme_service import OrganismeService


class ResetDatabase(metaclass=Singleton):
    """

    Initialisation de la vraie base de données.

    """

    @log
    def lancer(self):
        """

        Crée le schéma et les tables SQL.

        Parameters
        ----------
        verif : bool
            Ne crée le schéma et les tables que si c'est voulu.

        """

        os.environ["POSTGRES_SCHEMA"] = "statagora"

        dotenv.load_dotenv()
        schema = os.environ["POSTGRES_SCHEMA"]
        create_schema = (
            f"DROP SCHEMA IF EXISTS {
            schema} CASCADE;"
            f"CREATE SCHEMA {schema};"
        )
        with open("data/init_db.sql", encoding="utf-8") as init_db:
            init_db_as_string = init_db.read()
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
        except Exception as e:
            logging.error(e)
            raise

    @log
    def remplir(self):
        """

        Remplit les tables SQL.

        """

        publications_dares = DaresClient().get_all_dares(True)
        publications = publications_dares
        for publi in publications:
            PublicationService().creer(publi)
        print("La table 'publication' a bien été remplie.")
        OrganismeService().creer("dares")
        print("La table 'organisme' a bien été remplie.")


if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().remplir()
