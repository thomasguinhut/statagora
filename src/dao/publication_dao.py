import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.dao.db_connection import DBConnection
import logging

from src.utils.log_decorator import log


class PublicationDao:

    def __init__(self, df=None):
        self.df = df

    @log
    def informations_base(self, id_organisme) -> tuple[str, int, bool, int, str]:
        if not self.df.empty:
            df_organisme = self.df[self.df["id_organisme_publication"] == id_organisme]
            # Remplir les valeurs None avec une chaîne de caractères vide pour éviter les comparaisons invalides
            df_organisme["date_publication"] = df_organisme["date_publication"].fillna("")
            # S'assurer que toutes les dates sont des chaînes de caractères
            df_organisme["date_publication"] = df_organisme["date_publication"].astype(str)
            date_plus_recente = (
                df_organisme["date_publication"].max() if not df_organisme.empty else None
            )
            nombre_publications = len(df_organisme)
            base_vide = nombre_publications == 0

            # Calcul du nombre de publications antérieures
            nombre_publications_anterieures = df_organisme[
                df_organisme["date_publication"] < date_plus_recente
            ].shape[0]

        else:
            date_plus_recente = None
            nombre_publications_anterieures = 0
            base_vide = True

        return (
            date_plus_recente,
            nombre_publications_anterieures,
            base_vide,
        )

    @log
    def rechercher_publications(self, mots_clés, n, id_organisme=None) -> list[str]:

        model = SentenceTransformer("all-MiniLM-L6-v2")

        if not self.df.empty:
            self.df["texte_complet"] = (
                self.df["titre_publication"]
                + " "
                + self.df["soustitre_publication"]
                + " "
                + self.df["date_publication"]
                + " "
                + self.df["collection_publication"]
            )
            embeddings_publications = model.encode(self.df["texte_complet"].tolist())

        # Filtrer les publications par id_organisme si fourni
        if id_organisme:
            df_filtre = self.df[self.df["id_organisme_publication"] == id_organisme]
        else:
            df_filtre = self.df

        # Encoder la requête utilisateur
        embedding_requete = model.encode([mots_clés])

        # Calculer la similarité cosinus entre la requête et les documents filtrés
        similarités = cosine_similarity(embedding_requete, embeddings_publications[df_filtre.index])

        # Ajouter la similarité au DataFrame filtré pour un classement facile
        df_filtre["similarité"] = similarités.flatten()

        # Trier les résultats par similarité décroissante
        df_trie = df_filtre.sort_values(by="similarité", ascending=False)

        # Extraire les mots clés de 5 lettres ou plus
        mots_clés_longs = set(mot for mot in mots_clés.split() if len(mot) >= 5)

        # Vérifier si les mots clés longs sont dans le titre ou le sous-titre
        titres_prioritaires = df_filtre[
            df_filtre.apply(
                lambda row: any(
                    mot in row["titre_publication"] or mot in row["soustitre_publication"]
                    for mot in mots_clés_longs
                ),
                axis=1,
            )
        ]["titre_publication"].tolist()

        # Obtenir les titres des publications triées par similarité
        titres_similaires = df_trie.head(n)["titre_publication"].tolist()

        # Combiner les listes en mettant les titres prioritaires en premier
        titres_final = titres_prioritaires + [
            titre for titre in titres_similaires if titre not in titres_prioritaires
        ]

        return titres_final[:n]

    @log
    def supprimer_publications(self, date, id_organisme):
        """
        Supprime les publications qui ont pour date_publication une date donnée et qui appartiennent à l'id_organisme spécifié.
        """
        df = self.df[
            ~(
                (self.df["date_publication"] == date)
                & (self.df["id_organisme_publication"] == id_organisme)
            )
        ]
        DBConnection().enregistrer_feuille(df, id_organisme)
        return df
