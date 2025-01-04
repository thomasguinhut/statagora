import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from datetime import datetime
import locale
import logging

from src.utils.log_decorator import log


class DaresClient:
    BASE_URL = "https://dares.travail-emploi.gouv.fr/publications"

    def __init__(self) -> None:
        self.article_data: List[dict] = []

    @log
    def publications_dares(self, page_number: int) -> List[BeautifulSoup]:
        url = f"{self.BASE_URL}?page={page_number}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête HTTP: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article")
        return articles

    @log
    def publications_dares_dict(self, test: bool = False) -> List[dict]:
        page_number = 0
        empty_pages = 0

        while True:
            articles = self.publications_dares(page_number)

            if not articles:
                empty_pages += 1
                print(f"Page {page_number} vide. Compteur de pages vides : {empty_pages}")
                if empty_pages >= 2:
                    print(f"Fin des pages après {empty_pages} pages vides consécutives.")
                    break
            else:
                empty_pages = 0

            for article in articles:
                title, date, link, subtitle, collection = self.articles_infos(article)

                if title or date or link or subtitle or collection:
                    self.article_data.append(
                        {
                            "titre_publication": title,
                            "date_str_publication": date,
                            "lien_publication": (
                                f"https://dares.travail-emploi.gouv.fr{link}" if link else None
                            ),
                            "id_organisme_publication": "dares",
                            "soustitre_publication": subtitle,
                            "collection_publication": collection,
                        }
                    )

            page_number += 1

            if test and page_number == 4:
                return self.article_data

        return self.article_data

    @log
    def articles_infos(
        self, article
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
        title, date, link, subtitle, collection = None, None, None, None, None

        title_tag = article.find("h3", class_="list-article-title")
        if title_tag:
            title_link = title_tag.find("a")
            if title_link:
                title = title_link.get_text(strip=True).replace("\xa0", " ")
                link = title_link["href"]

        date_tag = article.find("ul", class_="list-article-information")
        if date_tag:
            date_span = date_tag.find("li", class_="list-item").find("span")
            if date_span:
                date = self.convertir_date(date_span.get_text(strip=True))

        subtitle_tag = article.find("p", class_="list-article-text")
        if subtitle_tag:
            subtitle = subtitle_tag.get_text(strip=True).replace("\xa0", " ")

        collection_tag = article.find("li", class_="list-item-alternative")
        if collection_tag:
            collection = " ".join(collection_tag.stripped_strings)

        return title, date, link, subtitle, collection

    @log
    def convertir_date(self, date_str):
        mois = {
            "janvier": "01",
            "février": "02",
            "mars": "03",
            "avril": "04",
            "mai": "05",
            "juin": "06",
            "juillet": "07",
            "août": "08",
            "septembre": "09",
            "octobre": "10",
            "novembre": "11",
            "décembre": "12",
        }

        jour, mois_str, annee = date_str.split()
        mois_num = mois[mois_str]
        jour = jour.zfill(2)  # Ajoute un zéro devant le jour si nécessaire
        return f"{jour}/{mois_num}/{annee}"
