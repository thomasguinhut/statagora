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

    def nombre_publications_a_ajouter(self, id_organisme):
        """
        Donne le nombre de publications à ajouter.

        Args:
            id_organisme (str)

        Returns:
            int
        """
        publications = DaresClient().get_all_dares(True)
        nouvelles_publications = []
        base_vide = PublicationService().base_vide()
        date_la_plus_récente_base = PublicationService().afficher_date_la_plus_récente_base("dares")
        p = 1
        n_base = PublicationService().nombre_publications("dares")
        n_publi = len(publications)
        for publication in publications:
            nouvelle_publication = PublicationService().creer_publications(publication)
            if base_vide:
                nouvelle_publication.id_publication = "dares_" + str(n_publi - p + 1)
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelle_publication.id_publication = "dares_" + str(n_base + n_publi - p + 1)
                    nouvelles_publications.append(nouvelle_publication.__dict__)
            p += 1
        return len(nouvelles_publications)

    def nombre_publications_anterieures(self, id_organisme):
        """
        Donne le nombre de publications dans la base avec une date strictement inférieure à la date la plus récente de la base.

        Args:
            id_organisme (str)

        Returns:
            int
        """
        date_la_plus_recente_base = PublicationService().afficher_date_la_plus_récente_base(
            id_organisme
        )
        publications = PublicationService().afficher_publications_organisme(id_organisme)
        count = 0
        for publication in publications:
            if publication.date_publication < date_la_plus_recente_base:
                count += 1
        return count

    @log
    def reset_publications_dares(self, test):
        publications = DaresClient().get_all_dares(test)
        nouvelles_publications = []
        base_vide = PublicationService().base_vide()
        date_la_plus_récente_base = PublicationService().afficher_date_la_plus_récente_base("dares")
        p = 1
        n_base = self.nombre_publications_anterieures("dares")
        n_publi = self.nombre_publications_a_ajouter("dares")
        for publication in publications:
            nouvelle_publication = PublicationService().creer_publications(publication)
            if base_vide:
                nouvelle_publication.id_publication = "dares_" + str(n_publi - p + 1)
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelle_publication.id_publication = "dares_" + str(n_base + n_publi - p + 1)
                    nouvelles_publications.append(nouvelle_publication.__dict__)
            p += 1
        df = pd.DataFrame(nouvelles_publications)
        sheet = DBConnection().connection()
        worksheet = sheet.worksheet("publications")
        worksheet.update("A1", [df.columns.values.tolist()] + df.values.tolist())
        print("Les publications ont bien été ajoutées à la base de données.")


if __name__ == "__main__":
    ResetDatabase().nouvelle_publication("dares")
