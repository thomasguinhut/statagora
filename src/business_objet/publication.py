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
        self.id = self.construire_id(self.organisme, self.collection, self.date)

    def construire_id(self, organisme, collection, date):
        """Construire un identifiant unique à partir de la collection et de la date."""

        # Mettre la collection en minuscules
        collection_modifiee = collection.lower()

        # Extraire tous les mots ayant plus de 4 lettres
        mots_collection_filtres = [mot for mot in collection_modifiee.split() if len(mot) > 4]

        # Mettre l'orgnaisme en minuscules
        organisme_modifie = organisme.lower()

        # Extraire tous les mots ayant plus de 4 lettres
        mots_organisme_filtres = [mot for mot in organisme_modifie.split()]

        # Ajouter les chiffres s'il y en a dans la collection
        chiffres = re.findall(r"\d+", collection)
        if chiffres:
            mots_collection_filtres += chiffres  # Ajouter les chiffres à la liste des mots filtrés

        # Construire l'ID en concatenant la date et les mots filtrés de la collection
        id_construit = (
            "_".join(mots_organisme_filtres)
            + "_"
            + date.replace("-", "")
            + "_"
            + "_".join(mots_collection_filtres)
        )

        return id_construit
