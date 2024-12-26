from src.business_objet.publication import Publication


def test_publication():
    publication = Publication(
        "Le titre de l'article",
        "2021-01-01",
        "http://example.com",
        "Dares",
        "Sous-titre de l'article",
        "Dares Focus N° 58",
    )
    assert publication.id == "dares_20210101_dares_focus_58"
