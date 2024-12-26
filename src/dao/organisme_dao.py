import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class OrganismeDao:

    @log
    def creer(self, organisme: str):
        image_path = f"/Users/thomasguinhut/Documents/statagora/data/logos/{organisme}.png"
        with open(image_path, "rb") as file:
            image_data = file.read()
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Remplacer '1' par l'identifiant ou le nom correct de l'organisme si nécessaire
                    cursor.execute(
                        "UPDATE organisme SET logo = %s WHERE nom_organisme = %s",
                        (image_data, "dares"),
                    )
                connection.commit()
                print("Image insérée avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")
        finally:
            connection.close()
