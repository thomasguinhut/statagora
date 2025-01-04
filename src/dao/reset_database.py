import time
from src.client.dares_client import DaresClient
from src.client.ssmsi_client import SsmsiClient
from src.service.publication_service import PublicationService
import pandas as pd
from src.dao.db_connection import DBConnection
import datetime
import logging
import os

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
        client, method = self.client_et_methode(id_organisme)
        publications = getattr(client, method)(test)
        nouvelles_publications = []
        publication_service = PublicationService(df)
        informations_base = publication_service.informations_base(id_organisme)
        base_vide = informations_base["base_vide"]
        date_la_plus_récente_base = informations_base["date_la_plus_recente"]

        for publication in publications:
            nouvelle_publication = publication_service.creer_publications(publication)
            if base_vide or nouvelle_publication.date_publication >= date_la_plus_récente_base:
                nouvelles_publications.append(nouvelle_publication.__dict__)

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
        n_publis_a_ajouter = self.nombre_publications_a_ajouter(df, test, id_organisme)
        n_publis_anterieures = informations_base["nombre_publications_anterieures"]

        if not base_vide:
            df = publication_service.supprimer_publications(date_la_plus_récente_base, id_organisme)

        nouvelles_publications = []
        p = 1

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
        df = pd.concat([pd.DataFrame(nouvelles_publications), df], ignore_index=True)
        DBConnection().enregistrer_feuille(df, id_organisme)

    @log
    def reset_publications(self, test=False):
        """
        Réinitialise les publications pour tous les organismes.

        Args:
            df (DataFrame): Le DataFrame contenant les publications.
            test (bool): Indicateur de test.
        """
        organismes = ["dares", "ssmsi"]
        for organisme in organismes:
            df = DBConnection().afficher_feuille(organisme)
            self.reset_publications_organisme(df, test, organisme)

    @log
    def doit_reset(self):
        """
        Vérifie si l'importation du fichier spécifié doit être effectuée en
        fonction de la date et de l'heure de la dernière importation de ce
        fichier (durée maximale entre deux importations que l'on se fixe :
        1 heure)
        """
        dossier_courant = os.path.abspath(os.path.dirname(__file__))
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.join(dossier_courant, "data/derniere_importation_fichier.txt")

        if not os.path.exists(dossier_courant):
            # Si le fichier xlm n'existe pas, l'importation est nécessaire
            return True
        # Lire la date de la dernière importation depuis le fichier de contrôle
        with open(dossier_courant, "r") as fichier:
            date = fichier.read()
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date_actuelle = datetime.datetime.now()
            duree = date_actuelle - date
            return duree.seconds > 3600

    @log
    def enregistrer_date_derniere_ouverture(self):
        """
        Enregistre la date d'aujourd'hui dans un fichier de contrôle.
        """
        dossier_courant = os.path.abspath(os.path.dirname(__file__))
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.join(dossier_courant, "data/derniere_importation_fichier.txt")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(dossier_courant, "w") as fichier:
            fichier.write(date)
