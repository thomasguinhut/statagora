import re
from datetime import datetime, date
import locale


class Publication:

    def __init__(
        self, titre: str, date_str: str, lien: str, organisme: str, soustitre: str, collection: str
    ):
        if isinstance(date_str, str) and date_str[2] == "/":
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        else:  # c'est déjà un obj
            date_obj = date_str
        if not isinstance(titre, str):
            raise TypeError("titre doit être un str")
        if not isinstance(date_obj, date):
            raise TypeError("date doit être une instance de datetime.date")
        if not isinstance(lien, str):
            raise TypeError("lien doit être un str")
        if not isinstance(organisme, str):
            raise TypeError("organisme doit être un str")
        if not isinstance(soustitre, str):
            raise TypeError("soustitre doit être un str")
        if not isinstance(collection, str):
            raise TypeError("collection doit être un str")

        collection = re.sub(r"([Nn])\s*°", r"\1°", collection)  # Cas 1
        collection = re.sub(r"([Nn]°)\s+(\d+)", r"\1\2", collection)  # Cas 2

        self.titre = titre
        self.date = date_obj
        self.lien = lien
        self.organisme = organisme
        self.soustitre = soustitre
        self.collection = collection

    def get_month_year_and_week(self):
        # Définir la locale en français pour afficher les mois en français
        try:
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")  # Réglage de la locale sur le français
        except locale.Error:
            print(
                "La locale 'fr_FR.UTF-8' n'est pas disponible. Assurez-vous qu'elle est installée sur votre système."
            )
            return None, None

        month_year = self.date.strftime(
            "%B %Y"
        ).capitalize()  # Mettre en majuscule la première lettre du mois
        week_number = self.date.strftime(
            "%V"
        )  # Numéro de semaine ISO (lundi comme premier jour de la semaine)
        return month_year, int(week_number)


if __name__ == "__main__":
    publication = Publication(
        titre="Titre",
        date_str="31/12/2024",
        lien="lien",
        organisme="organisme",
        soustitre="soustitre",
        collection="123",
    )
    print(publication.get_month_year_and_week())
