import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class PublicationDao:

    @log
    def creer(self, publication) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO publication(titre_publication,
                                                date_publication, lien_publication,
                                                organisme_publication, soustitre_publication,
                                                collection_publication) VALUES
                        (%(titre_publication)s, %(date_publication)s,
                        %(lien_publication)s, %(organisme_publication)s,
                        %(soustitre_publication)s, %(collection_publication)s)
                            RETURNING titre_publication;
                        """,
                        {
                            "titre_publication": publication.titre,
                            "date_publication": publication.date,
                            "lien_publication": publication.lien,
                            "organisme_publication": publication.organisme,
                            "soustitre_publication": publication.soustitre,
                            "collection_publication": publication.collection,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise
        created = False
        if res:
            created = True
        return created
