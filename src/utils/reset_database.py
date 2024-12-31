import logging

from src.utils.log_decorator import log
from src.client.dares_client import DaresClient
from src.service.publication_service import PublicationService
import pandas as pd
from src.dao.db_connection import DBConnection


class ResetDatabase:
    """

    Initialisation de la vraie base de données.

    """

    @log
    def nouvelle_publication(self, id_organisme) -> bool:
        """
        Dit s'il y a de nouvelles publications d'un organisme.

        Args:
            id_organisme (str)

        Returns:
            bool
        """

        date_la_plus_récente_base = PublicationService().afficher_date_la_plus_récente_base(
            id_organisme
        )

        # Vérifier si la base est vide
        if date_la_plus_récente_base is None:
            raise Exception("La base de données est vide.")

        if id_organisme == "dares":
            date_la_plus_récente_publi = DaresClient().get_first_publication_date()
            return date_la_plus_récente_publi > date_la_plus_récente_base

    @log
    def reset_publications(self, test):
        publications = DaresClient().get_all_dares(test)
        nouvelles_publications = []
        base_vide = PublicationService().base_vide()
        for publication in publications:
            nouvelle_publication = PublicationService().creer_publications(publication)
            if base_vide:
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                date_la_plus_récente_base = PublicationService().afficher_date_la_plus_récente_base(
                    nouvelle_publication.id_organisme_publication
                )
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelles_publications.append(nouvelle_publication.__dict__)
        df = pd.DataFrame(nouvelles_publications)
        sheet = DBConnection().connection()
        worksheet = sheet.worksheet("publications")
        worksheet.update("A1", [df.columns.values.tolist()] + df.values.tolist())
        print("Les publications ont bien été ajoutées à la base de données.")


if __name__ == "__main__":
    ResetDatabase().nouvelle_publication("dares")
