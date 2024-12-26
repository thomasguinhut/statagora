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
        self.id = self.construire_id(self.titre, self.organisme, self.collection, self.date)

    def construire_id(self, titre, organisme, collection, date):
        """Construire un identifiant unique à partir de la collection et de la date."""

        # Partie collection
        collection_modifiee = collection.lower()
        mots_collection_filtres = [mot for mot in collection_modifiee.split() if len(mot) > 4]

        # Ajouter les chiffres s'il y en a dans la collection
        chiffres = re.findall(r"\d+", collection)
        if chiffres:
            mots_collection_filtres += chiffres  # Ajouter les chiffres à la liste des mots filtrés

        # Partie organisme
        organisme_modifie = organisme.lower()
        mots_organisme_filtres = [mot for mot in organisme_modifie.split()]

        # Partie titre
        titre_modifie = titre.lower()
        mots_titre_filtres = [mot[0] for mot in titre_modifie.split() if len(mot) > 4]

        # Construire l'ID en concatenant la date et les mots filtrés de la collection
        id_construit = (
            "_".join(mots_organisme_filtres)
            + "_"
            + date.replace("-", "")
            + "_"
            + "_".join(mots_collection_filtres)
            + "_"
            + "".join(mots_titre_filtres)
        )

        return id_construit


if __name__ == "__main__":
    publication = Publication(
        "Le titre de l'article",
        "2021-01-01",
        "http://example.com",
        "Dares",
        "Sous-titre de l'article",
        "Dares Focus N° 58",
    )
    print(publication.id)
