import time
from src.client.dares_client import DaresClient
from src.client.ssmsi_client import SsmsiClient
from src.service.publication_service import PublicationService
import pandas as pd
from src.dao.db_connection import DBConnection
import datetime
import os
import logging

from src.utils.log_decorator import log


class ResetDatabase:
    """
    Initialisation de la vraie base de données.
    """

    @log
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
        elif id_organisme == "ssmsi":
            return SsmsiClient(), "publications_ssmsi_dict"
        else:
            raise ValueError(f"Organisme inconnu: {id_organisme}")

    @log
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
        for publication in publications:
            nouvelle_publication = publication_service.creer_publications(publication)
            if base_vide:
                nouvelles_publications.append(nouvelle_publication.__dict__)
            else:
                if nouvelle_publication.date_publication >= date_la_plus_récente_base:
                    nouvelles_publications.append(nouvelle_publication.__dict__)
            p += 1
        return len(nouvelles_publications)

    @log
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

        try:
            if base_vide:
                worksheet.update("A1", [df.columns.values.tolist()] + df.values.tolist())
            else:
                existing_data = worksheet.get_all_values()
                new_data = [df.columns.values.tolist()] + df.values.tolist() + existing_data[1:]
                worksheet.update("A1", new_data)
            print(f"Les publications '{id_organisme}' ont été réinitialisées.")
        except OSError as e:
            print(
                f"Erreur d'entrée/sortie lors de la mise à jour des publications pour l'organisme {id_organisme} : {e}"
            )
            raise

    @log
    def reset_publications(self, df, test=False):
        try:
            self.reset_publications_organisme(df, test, "dares")
            self.reset_publications_organisme(df, test, "ssmsi")
        except OSError as e:
            print(f"Erreur d'entrée/sortie lors de la réinitialisation des publications : {e}")
            raise

    @log
    def doit_reset(self):
        """
        Vérifie si l'importation du fichier spécifié doit être effectuée en
        fonction de la date et de l'heure de la dernière importation de ce
        fichier (durée maximale entre deux importations que l'on se fixe :
        1 heure)
        """
        worksheet = DBConnection().connection("dernier_reset")
        date_cell = worksheet.get("A1")
        if not date_cell or not date_cell[0]:
            return True
        date = date_cell[0][0]
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_actuelle = datetime.datetime.now()
        duree = date_actuelle - date
        return duree.seconds > 360

    @log
    def enregistrer_date_derniere_ouverture(self):
        """
        Enregistre la date d'aujourd'hui dans un fichier de contrôle.
        """
        worksheet = DBConnection().connection("dernier_reset")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.update("A1", [[date]])
