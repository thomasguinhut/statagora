import logging
from src.dao.db_connection import DBConnection
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class PublicationDao:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        sheet = DBConnection().connection()
        sheet_info = sheet.worksheet("publications")
        records = sheet_info.get_all_records()
        self.df = pd.DataFrame(records)
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
            self.embeddings_publications = self.model.encode(self.df["texte_complet"].tolist())

    def afficher_publications(self):
        return self.df

    def afficher_date_la_plus_récente_base(self, id_organisme):
        df = self.afficher_publications()
        if not df.empty:
            df = df[df["id_organisme_publication"] == id_organisme]
            return df["date_publication"].max()
        else:
            return None

    def rechercher_publications(self, mots_clés, n):
        # Encoder la requête utilisateur
        embedding_requete = self.model.encode([mots_clés])

        # Calculer la similarité cosinus entre la requête et les documents
        similarités = cosine_similarity(embedding_requete, self.embeddings_publications)

        # Ajouter la similarité au DataFrame pour un classement facile
        self.df["similarité"] = similarités.flatten()

        # Trier les résultats par similarité décroissante
        df_trie = self.df.sort_values(by="similarité", ascending=False)

        # Extraire les mots clés de 5 lettres ou plus
        mots_clés_longs = [mot for mot in mots_clés.split() if len(mot) >= 5]

        # Liste pour les titres de publications à ajouter en priorité
        titres_prioritaires = []

        # Vérifier si les mots clés longs sont dans le titre ou le sous-titre
        for index, row in self.df.iterrows():
            for mot in mots_clés_longs:
                if mot in row["titre_publication"] or mot in row["soustitre_publication"]:
                    titres_prioritaires.append(row["titre_publication"])
                    break

        # Obtenir les titres des publications triées par similarité
        titres_similaires = df_trie.head(n)["titre_publication"].tolist()

        # Combiner les listes en mettant les titres prioritaires en premier
        titres_final = titres_prioritaires + [
            titre for titre in titres_similaires if titre not in titres_prioritaires
        ]

        return titres_final[:n]

    def base_vide(self) -> bool:
        """
        Vérifie si la base de données est vide.

        Returns:
            bool: True si la base est vide, False sinon.
        """
        return self.df.empty
