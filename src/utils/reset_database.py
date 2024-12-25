import os
import dotenv

from log_decorator import log
from singleton import Singleton
from src.dao.db_connection import DBConnection
from src.client.dares_client import DaresClient
from src.service.dares_service import DaresService


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
        create_schema = f"DROP SCHEMA IF EXISTS {
            schema} CASCADE;" f"CREATE SCHEMA {schema};"
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

        publications_dares = DaresClient().get_all_dares()
        for publi in publi_dares:
            DaresService().creer(publi)
        print("La table 'dares' a bien été remplie.")


if __name__ == "__main__":
    ResetDatabase().lancer()
