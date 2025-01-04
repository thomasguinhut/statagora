import time
from src.client.dares_client import DaresClient
from src.client.ssmsi_client import SsmsiClient
from src.service.publication_service import PublicationService
import pandas as pd
from src.dao.db_connection import DBConnection
import datetime
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

        Returns:
            list: Liste des nouvelles publications.
        """
        client, method = self.client_et_methode(id_organisme)
        publications = getattr(client, method)(test)
        publication_service = PublicationService(df)
        informations_base = publication_service.informations_base(id_organisme)
        date_la_plus_récente_base = informations_base["date_la_plus_recente"]
        base_vide = informations_base["base_vide"]

        if not base_vide:
            publication_service.supprimer_publications(date_la_plus_récente_base, id_organisme)

        nouvelles_publications = []
        n_publis_anterieures = informations_base["nombre_publications_anterieures"]
        n_publis_a_ajouter = self.nombre_publications_a_ajouter(df, test, id_organisme)

        for p, publication in enumerate(publications, start=1):
            nouvelle_publication = publication_service.creer_publications(publication)
            if base_vide:
                nouvelle_publication.id_publication = f"{id_organisme}_{n_publis_a_ajouter - p + 1}"
            elif nouvelle_publication.date_publication >= date_la_plus_récente_base:
                nouvelle_publication.id_publication = (
                    f"{id_organisme}_{n_publis_anterieures + n_publis_a_ajouter - p + 1}"
                )
            nouvelles_publications.append(nouvelle_publication.__dict__)

        return nouvelles_publications

    @log
    def reset_publications(self, df, test=False):
        """
        Réinitialise les publications pour tous les organismes.

        Args:
            df (DataFrame): Le DataFrame contenant les publications.
            test (bool): Indicateur de test.
        """
        try:
            nouvelles_publications = []
            for id_organisme in ["dares", "ssmsi"]:
                nouvelles_publications += self.reset_publications_organisme(df, test, id_organisme)

            if nouvelles_publications:
                df = pd.DataFrame(nouvelles_publications)
                worksheet = DBConnection().connection("publications")
                existing_data = worksheet.get_all_values()
                new_data = [df.columns.values.tolist()] + df.values.tolist() + existing_data[1:]
                worksheet.update("A1", new_data)
                print("Les publications ont été réinitialisées.")
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
        return duree.seconds > 3600

    @log
    def enregistrer_date_derniere_ouverture(self):
        """
        Enregistre la date d'aujourd'hui dans un fichier de contrôle.
        """
        worksheet = DBConnection().connection("dernier_reset")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.update("A1", [[date]])

    @log
    def trier_publications(self, df):
        """
        Trie les publications par date de publication.

        Args:
            df (DataFrame): Le DataFrame contenant les publications.
        """
        if not df.empty and "date_publication" in df.columns:
            df["date_publication"] = pd.to_datetime(df["date_publication"])
            df = df.sort_values(by="date_publication", ascending=False)
        else:
            print("Le DataFrame est vide ou la colonne 'date_publication' n'existe pas.")

        # Convertir les objets Timestamp en chaînes de caractères
        df = df.astype(str)

        worksheet = DBConnection().connection("publications")
        worksheet.clear()
        worksheet.update("A1", [df.columns.values.tolist()] + df.values.tolist())
        print("Les publications ont été triées par date de publication.")
