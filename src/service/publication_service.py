from business_objet.publication import Publication
from dao.publication_dao import PublicationDao

from utils.log_decorator import log


class PublicationService:

    @log
    def creer(self, publication: dict[str, str]) -> Publication:

        nouvelle_publication = Publication(
            titre=publication["titre"],
            date=publication["date"],
            lien=publication["lien"],
            organisme=publication["organisme"],
            soustitre=publication["soustitre"],
            collection=publication["collection"],
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
                titre=row.titre_publication,
                date=row.date_publication,
                lien=row.lien_publication,
                organisme=row.organisme_publication,
                soustitre=row.soustitre_publication,
                collection=row.collection_publication,
            )
            liste.append(publi)
        return liste


if __name__ == "__main__":
    publication_service = PublicationService()
    print(publication_service.tout_afficher())
