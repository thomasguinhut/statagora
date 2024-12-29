import logging

from log_decorator import log
from client.dares_client import DaresClient
from service.publication_service import PublicationService
import pandas as pd
from dao.db_connection import DBConnection


class ResetDatabase:
    """

    Initialisation de la vraie base de données.

    """

    @log
    def reset_publications(self, test):
        publications = DaresClient().get_all_dares(test)
        nouvelles_publications = []
        for publication in publications:
            nouvelle_publication = PublicationService().creer_publications(publication)
            nouvelles_publications.append(nouvelle_publication.__dict__)
        df = pd.DataFrame(nouvelles_publications)
        sheet = DBConnection().connection()
        worksheet = sheet.worksheet("publications")
        worksheet.update(values=[df.columns.values.tolist()] + df.values.tolist(), range_name="A1")
        print("Les publications ont bien été ajoutées à la base de données.")


if __name__ == "__main__":
    # ResetDatabase().reset_publications(True)
    ResetDatabase().reset_organismes()
