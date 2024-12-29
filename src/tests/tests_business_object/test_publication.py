import unittest
from business_objet.publication import Publication
from datetime import datetime, date


class TestPublication(unittest.TestCase):

    def test_titre_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication=123,
                date_str_publication="2024-12-26",
                lien_publication="lien",
                id_organisme_publication="organisme",
                soustitre_publication="soustitre",
                collection_publication="collection",
            )
        self.assertEqual(str(context.exception), "titre_publication doit être un str")

    def test_date_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication=123,
                lien_publication="lien",
                id_organisme_publication="organisme",
                soustitre_publication="soustitre",
                collection_publication="collection",
            )
        self.assertEqual(
            str(context.exception),
            "date_str_publication doit être un str",
        )

    def test_date_bon_format(self):
        with self.assertRaises(ValueError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication="123",
                lien_publication="lien",
                id_organisme_publication="organisme",
                soustitre_publication="soustitre",
                collection_publication="collection",
            )

    def test_lien_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication="2024-12-26",
                lien_publication=123,
                id_organisme_publication="organisme",
                soustitre_publication="soustitre",
                collection_publication="collection",
            )
        self.assertEqual(str(context.exception), "lien_publication doit être un str")

    def test_id_organisme_publication_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication="2024-12-26",
                lien_publication="lien",
                id_organisme_publication=123,
                soustitre_publication="soustitre",
                collection_publication="collection",
            )
        self.assertEqual(str(context.exception), "id_organisme_publication doit être un str")

    def test_soustitre_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication="2024-12-26",
                lien_publication="lien",
                id_organisme_publication="organisme",
                soustitre_publication=123,
                collection_publication="collection",
            )
        self.assertEqual(str(context.exception), "soustitre_publication doit être un str")

    def test_collection_non_string(self):
        with self.assertRaises(TypeError) as context:
            publication = Publication(
                titre_publication="Titre",
                date_str_publication="2024-12-26",
                lien_publication="lien",
                id_organisme_publication="organisme",
                soustitre_publication="soustitre",
                collection_publication=123,
            )
        self.assertEqual(str(context.exception), "collection_publication doit être un str")

    def test_date_publication_type(self):
        publication = Publication(
            titre_publication="Titre",
            date_str_publication="26/12/2024",
            lien_publication="lien",
            id_organisme_publication="organisme",
            soustitre_publication="soustitre",
            collection_publication="collection",
        )
        self.assertIsInstance(publication.date_publication, date)

    def test_get_month_year_and_week(self):
        publication = Publication(
            titre_publication="Titre",
            date_str_publication="26/12/2024",
            lien_publication="lien",
            id_organisme_publication="organisme",
            soustitre_publication="soustitre",
            collection_publication="collection",
        )
        self.assertEqual(publication.get_month_year_and_week(), ("Décembre 2024", 52))


if __name__ == "__main__":
    unittest.main()
