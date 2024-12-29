from business_objet.publication import Publication
from dao.publication_dao import PublicationDao

from utils.log_decorator import log


class PublicationService:

    @log
    def creer(self, publication: dict[str, str]) -> Publication:

        nouvelle_publication = Publication(
            titre_publication=publication["titre_publication"],
            date_str_publication=publication["date_str_publication"],
            lien_publication=publication["lien_publication"],
            id_organisme_publication=publication["id_organisme_publication"],
            soustitre_publication=publication["soustitre_publication"],
            collection_publication=publication["collection_publication"],
        )

        if PublicationDao().creer(nouvelle_publication):
            return nouvelle_publication
        else:
            return None

    def tout_afficher(self):
        df = PublicationDao().tout_afficher()
        liste = []
        for row in df.itertuples():
            publi = Publication(
                titre_publication=row.titre_publication,
                date_str_publication=row.date_publication,
                lien_publication=row.lien_publication,
                id_organisme_publication=row.organisme_publication,
                soustitre_publication=row.soustitre_publication,
                collection_publication=row.collection_publication,
            )
            liste.append(publi)
        return liste

    def afficher_date_la_plus_récente(self, organisme):
        return PublicationDao().afficher_date_la_plus_récente(organisme)

    def nom_explicite_organisme(self, id_organisme):
        return PublicationDao().nom_explicite_organisme(id_organisme)


if __name__ == "__main__":
    publication_service = PublicationService()
    print(publication_service.afficher_date_la_plus_récente("dares"))
