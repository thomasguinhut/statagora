import os
import dotenv
import logging

from log_decorator import log
from singleton import Singleton
from dao.db_connection import DBConnection
from client.dares_client import DaresClient
from service.publication_service import PublicationService


class ResetDatabase(metaclass=Singleton):
    """

    Initialisation de la vraie base de données.

    """

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


if __name__ == "__main__":
    ResetDatabase().remplir()
