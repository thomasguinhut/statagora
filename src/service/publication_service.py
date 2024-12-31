from src.business_objet.publication import Publication
from src.dao.publication_dao import PublicationDao

from src.utils.log_decorator import log


class PublicationService:

    @log
    def creer_publications(self, publication: dict):
        nouvelle_publication = Publication(
            titre_publication=publication["titre_publication"],
            date_str_publication=publication["date_str_publication"],
            lien_publication=publication["lien_publication"],
            id_organisme_publication=publication["id_organisme_publication"],
            soustitre_publication=publication["soustitre_publication"],
            collection_publication=publication["collection_publication"],
        )
        return nouvelle_publication

    def afficher_publications(self):
        df = PublicationDao().afficher_publications()
        liste = []
        for row in df.itertuples():
            if row:
                publi = Publication(
                    titre_publication=row.titre_publication,
                    date_str_publication=row.date_publication,
                    lien_publication=row.lien_publication,
                    id_organisme_publication=row.id_organisme_publication,
                    soustitre_publication=row.soustitre_publication,
                    collection_publication=row.collection_publication,
                )
                print(publi.titre_publication)
                liste.append(publi)
            liste = None
        return liste

    def afficher_publications_organisme(self, id_organisme):
        df = PublicationDao().afficher_publications()
        liste = []
        for row in df.itertuples():
            if row and row.id_organisme_publication == id_organisme:
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

    def afficher_date_la_plus_récente_base(self, id_organisme):
        return PublicationDao().afficher_date_la_plus_récente_base(id_organisme)

    def rechercher_publications(self, mots_clés, n):
        return PublicationDao().rechercher_publications(mots_clés, n)

    def base_vide(self):
        return PublicationDao().base_vide()

    def nombre_publications(self, id_organisme):
        return PublicationDao().nombre_publications(id_organisme)


if __name__ == "__main__":
    publication_service = PublicationService()
    print(publication_service.afficher_date_la_plus_récente("dares"))
