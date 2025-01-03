from src.business_objet.publication import Publication
from src.dao.publication_dao import PublicationDao
import logging

from src.utils.log_decorator import log


class PublicationService:

    def __init__(self, df=None):
        self.df = df

    @log
    def creer_publications(self, publication: dict) -> Publication:
        nouvelle_publication = Publication(
            titre_publication=publication["titre_publication"],
            date_str_publication=publication["date_str_publication"],
            lien_publication=publication["lien_publication"],
            id_organisme_publication=publication["id_organisme_publication"],
            soustitre_publication=publication["soustitre_publication"],
            collection_publication=publication["collection_publication"],
        )
        return nouvelle_publication

    @log
    def afficher_publications(self) -> list[Publication]:
        liste = []
        for row in self.df.itertuples():
            if row:
                publi = Publication(
                    titre_publication=row.titre_publication,
                    date_str_publication=row.date_publication,
                    lien_publication=row.lien_publication,
                    id_organisme_publication=row.id_organisme_publication,
                    soustitre_publication=row.soustitre_publication,
                    collection_publication=row.collection_publication,
                )
                liste.append(publi)
        return liste

    @log
    def afficher_publications_organisme(self, id_organisme) -> list[Publication]:
        liste = []
        for row in self.df.itertuples():
            if row and row.id_organisme_publication == id_organisme:
                publi = Publication(
                    titre_publication=row.titre_publication,
                    date_str_publication=row.date_publication,
                    lien_publication=row.lien_publication,
                    id_organisme_publication=row.id_organisme_publication,
                    soustitre_publication=row.soustitre_publication,
                    collection_publication=row.collection_publication,
                )
                liste.append(publi.titre_publication)
        return liste

    @log
    def informations_base(self, id_organisme):
        informations = PublicationDao(self.df).informations_base(id_organisme)
        return {
            "date_la_plus_recente": informations[0],
            "nombre_publications_anterieures": informations[1],
            "base_vide": informations[2],
        }

    @log
    def rechercher_publications(self, mots_clés, n, id_organisme=None) -> list[str]:
        return PublicationDao(self.df).rechercher_publications(mots_clés, n, id_organisme)

    @log
    def supprimer_publications(self, date, id_organisme):
        return PublicationDao(self.df).supprimer_publications(date, id_organisme)
