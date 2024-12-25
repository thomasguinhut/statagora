from src.business_objet.publication import Publication

from src.utils.log_decorator import log


class PublicationService:

    @log
    def creer(self, publication: dict[str, str]) -> Publication:

        nouvelle_publication = Publication(
            titre=publication['titre'],
            date=publication['date'],
            lien=publication['lien'],
            organisme=publication['organisme'],
            soustitre=publication['soustitre'],
            collection=publication['collection'],
        )

        return nouvelle_publication
