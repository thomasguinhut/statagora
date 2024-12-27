import unittest
from business_objet.publication import Publication


class TestPublication(unittest.TestCase):

    def test_titre_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre=123,
                date_str="2024-12-26",
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
                date_str=123,
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
                date_str="2024-12-26",
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
                date_str="2024-12-26",
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
                date_str="2024-12-26",
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
                date_str="2024-12-26",
                lien="lien",
                organisme="organisme",
                soustitre="soustitre",
                collection=123,
            )
        self.assertEqual(str(context.exception), "collection doit être un str")
