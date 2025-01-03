import time
from src.client.dares_client import DaresClient
from src.service.publication_service import PublicationService
import pandas as pd
from src.dao.db_connection import DBConnection
import datetime
import os


class ResetDatabase:
    """
    Initialisation de la vraie base de données.
    """

    def client_et_methode(self, id_organisme):
        """
        Retourne le client et la méthode appropriés en fonction de l'identifiant de l'organisme.

        Args:
            id_organisme (str): L'identifiant de l'organisme.

        Returns:
            tuple: (client, method)
        """
        if id_organisme == "dares":
            return DaresClient(), "publications_dares_dict"
        elif id_organisme == "insee":
            return InseeClient(), "publications_insee_dict"
        else:
            raise ValueError(f"Organisme inconnu: {id_organisme}")

    def nombre_publications_a_ajouter(self, df, test, id_organisme):
        """
        Donne le nombre de publications à ajouter.

        Args:
            test (bool): Indicateur de test.
            id_organisme (str): L'identifiant de l'organisme.

        Returns:
            int
        """
        start_time = time.time()
        client, method = self.client_et_methode(id_organisme)
        publications = getattr(client, method)(test)
        nouvelles_publications = []
        publication_service = PublicationService(df)
        informations_base = publication_service.informations_base(id_organisme)
        base_vide = informations_base["base_vide"]
        date_la_plus_récente_base = informations_base["date_la_plus_recente"]
        p = 1
        print(publications)
        for publication in publications:
            nouvelle_publication = publication_service.creer_publications(publication)
            if base_vide:
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelles_publications.append(nouvelle_publication.__dict__)
            p += 1
        return len(nouvelles_publications)

    def reset_publications_organisme(self, df, test, id_organisme):
        """
        Réinitialise les publications pour un organisme donné.

        Args:
            test (bool): Indicateur de test.
            id_organisme (str): L'identifiant de l'organisme.
        """
        start_time = time.time()
        client, method = self.client_et_methode(id_organisme)
        publications = getattr(client, method)(test)
        publication_service = PublicationService(df)
        informations_base = publication_service.informations_base(id_organisme)
        date_la_plus_récente_base = informations_base["date_la_plus_recente"]
        base_vide = informations_base["base_vide"]
        if not base_vide:
            publication_service.supprimer_publications(date_la_plus_récente_base, id_organisme)

        nouvelles_publications = []
        p = 1
        n_publis_anterieures = informations_base["nombre_publications_anterieures"]
        n_publis_a_ajouter = self.nombre_publications_a_ajouter(df, test, id_organisme)

        for publication in publications:
            nouvelle_publication = publication_service.creer_publications(publication)
            if base_vide:
                nouvelle_publication.id_publication = f"{id_organisme}_{n_publis_a_ajouter - p + 1}"
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelle_publication.id_publication = (
                        f"{id_organisme}_{n_publis_anterieures + n_publis_a_ajouter - p + 1}"
                    )
                    nouvelles_publications.append(nouvelle_publication.__dict__)
            p += 1

        df = pd.DataFrame(nouvelles_publications)
        worksheet = DBConnection().connection("publications")

        if base_vide:
            worksheet.update("A1", [df.columns.values.tolist()] + df.values.tolist())
        else:
            existing_data = worksheet.get_all_values()
            new_data = [df.columns.values.tolist()] + df.values.tolist() + existing_data[1:]
            worksheet.update("A1", new_data)
        print(f"Les publications '{id_organisme}' ont été réinitialisées.")

    def reset_publications(self, df, test=False):
        self.reset_publications_organisme(df, test, "dares")
