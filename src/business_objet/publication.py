import re


class Publication:

    def __init__(
        self, titre: str, date: str, lien: str, organisme: str, soustitre: str, collection: str
    ):
        if not isinstance(titre, str):
            raise TypeError("titre doit être un str")
        if not isinstance(date, str):
            raise TypeError("date doit être un str")
        if not isinstance(lien, str):
            raise TypeError("lien doit être un str")
        if not isinstance(organisme, str):
            raise TypeError("organisme doit être un str")
        if not isinstance(soustitre, str):
            raise TypeError("soustitre doit être un str")
        if not isinstance(collection, str):
            raise TypeError("collection doit être un str")

        self.titre = titre
        self.date = date
        self.lien = lien
        self.organisme = organisme
        self.soustitre = soustitre
        self.collection = collection
