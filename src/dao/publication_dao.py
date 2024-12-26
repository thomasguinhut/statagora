import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from src.dao.db_connection import DBConnection


class PublicationDao:

    @log
    def creer(self, publication) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO publication(id_categorie, nom_categorie) VALUES
                        (%(titre_publication)s, %(date_publication)s,
                        %(lien_publication)s, %(organisme_publication)s,
                        %(soustitre_publication)s, %(collection_publication)s)
                            RETURNING titre_publication;
                        """,
                        {
                            "titre": publication.titre,
                            "date": publication.date,
                            "lien": publication.lien,
                            "organisme": publication.organisme,
                            "soustitre": publication.soustitre,
                            "collection": publication.collection,
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
