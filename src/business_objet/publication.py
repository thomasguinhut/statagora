import re
from datetime import datetime, date
import locale


class Publication:

    def __init__(
        self,
        titre_publication: str,
        date_str_publication: str,
        lien_publication: str,
        id_organisme_publication: str,
        soustitre_publication: str,
        collection_publication: str,
    ):
        date_obj = self.format_date(date_str_publication)
        if not isinstance(titre_publication, str):
            raise TypeError("titre_publication doit être un str")
        if not isinstance(lien_publication, str):
            raise TypeError("lien_publication doit être un str")
        if not isinstance(id_organisme_publication, str):
            raise TypeError("id_organisme_publication doit être un str")
        if not isinstance(soustitre_publication, str):
            raise TypeError("soustitre_publication doit être un str")
        if not isinstance(collection_publication, str):
            raise TypeError("collection_publication doit être un str")

        collection = re.sub(
            r"([Nn]°)\s+(\d+)", r"\1\2", collection_publication
        )  # N° 123" deviendra "N°123

        self.titre_publication = titre_publication
        self.date_publication = str(date_obj)
        self.lien_publication = lien_publication
        self.id_organisme_publication = id_organisme_publication
        self.nom_officiel_organisme = self.nom_officiel(id_organisme_publication)
        self.soustitre_publication = soustitre_publication
        self.collection_publication = collection

    def format_date(self, date_str_publication: str) -> date:
        """

        Transforme la date de publication en datetime.date

        Args:
            date_str_publication: str

        Raises:
            TypeError: vérifie que date_str_publication est un str
            ValueError: vérifie que date_str_publication est au format XX/XX/XXXX ou XXXX-XX-XX

        Returns:
            date: datetime.date
        """

        if not isinstance(date_str_publication, str):
            raise TypeError("date_str_publication doit être un str")
        if re.match(r"^\d{2}/\d{2}/\d{4}$", date_str_publication):
            return datetime.strptime(date_str_publication, "%d/%m/%Y").date()
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_str_publication):
            return datetime.strptime(date_str_publication, "%Y-%m-%d").date()
        else:
            raise ValueError(
                "date_str_publication doit être au format XX/XX/XXXX ou XXXX-XX-XX de datetime.date"
            )

    def get_month_year_and_week(self):
        try:
            # Définir la locale en français pour afficher les mois en français
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        except locale.Error:
            # Si la locale n'est pas supportée, utiliser la locale par défaut
            locale.setlocale(locale.LC_TIME, "C")

        date = datetime.strptime(self.date_publication, "%Y-%m-%d").date()
        month_year = date.strftime("%B %Y")
        week = date.isocalendar()[1]
        return month_year.capitalize(), week

    def nom_officiel(self, id_organisme: str) -> str:
        if id_organisme == "dares":
            return "Dares"
        elif id_organisme == "insee":
            return "Insee"
        elif id_organisme == "ssmsi":
            return "SSM-SI"

    def nettoyer_titre_et_soustitre(self):
        pass


if __name__ == "__main__":
    publication = Publication(
        titre_publication="Titre",
        date_str_publication="26/12/2024",
        lien_publication="lien",
        id_organisme_publication="dares",
        soustitre_publication="soustitre",
        collection_publication="collection",
    )
    print(publication.nom_officiel_organisme)
