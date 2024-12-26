import unittest
from src.business_objet.publication import Publication


class TestPublication(unittest.TestCase):

    def test_publication(self):
        publication = Publication(
            "Le titre de l'article",
            "2021-01-01",
            "http://example.com",
            "Dares",
            "Sous-titre de l'article",
            "Dares Focus N° 58",
        )
        # Test si l'ID généré est correct
        self.assertEqual(publication.id, "dares_20210101_dares_focus_58")

    def test_titre_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre=123,
                date="2024-12-26",
                lien="lien",
                organisme="organisme",
                soustitre="soustitre",
                collection="collection",
            )
        self.assertEqual(str(context.exception), "titre doit être un str")

    def test_date_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre="Titre",
                date=123,
                lien="lien",
                organisme="organisme",
                soustitre="soustitre",
                collection="collection",
            )
        self.assertEqual(str(context.exception), "date doit être un str")

    def test_lien_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre="Titre",
                date="2024-12-26",
                lien=123,
                organisme="organisme",
                soustitre="soustitre",
                collection="collection",
            )
        self.assertEqual(str(context.exception), "lien doit être un str")

    def test_organisme_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre="Titre",
                date="2024-12-26",
                lien="lien",
                organisme=123,
                soustitre="soustitre",
                collection="collection",
            )
        self.assertEqual(str(context.exception), "organisme doit être un str")

    def test_soustitre_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre="Titre",
                date="2024-12-26",
                lien="lien",
                organisme="organisme",
                soustitre=123,
                collection="collection",
            )
        self.assertEqual(str(context.exception), "soustitre doit être un str")

    def test_collection_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre="Titre",
                date="2024-12-26",
                lien="lien",
                organisme="organisme",
                soustitre="soustitre",
                collection=123,
            )
        self.assertEqual(str(context.exception), "collection doit être un str")
