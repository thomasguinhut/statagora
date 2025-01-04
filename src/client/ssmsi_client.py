import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from datetime import datetime
import logging

from src.utils.log_decorator import log


class SsmsiClient:
    BASE_URL = "https://www.interieur.gouv.fr/Interstats/Actualites"

    def __init__(self) -> None:
        self.article_data: List[dict] = []

    @log
    def publications_ssmsi(self, page_number: int) -> List[BeautifulSoup]:
        url = f"{self.BASE_URL}/(offset)/{page_number * 20}#79903_children"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête HTTP: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all(
            "div", class_=["content-view-line linkBloc first", "content-view-line linkBloc"]
        )
        return articles

    @log
    def publications_ssmsi_dict(self, test: bool = False) -> List[dict]:
        page_number = 0
        empty_pages = 0

        while True:
            articles = self.publications_ssmsi(page_number)

            if not articles:
                empty_pages += 1
                if empty_pages >= 2:
                    break
            else:
                empty_pages = 0

            for article in articles:
                title, date, link, subtitle = self.articles_infos(article)

                if title or date or link or subtitle:
                    self.article_data.append(
                        {
                            "titre_publication": title,
                            "date_str_publication": date,
                            "lien_publication": (
                                f"https://www.interieur.gouv.fr{link}" if link else None
                            ),
                            "id_organisme_publication": "ssmsi",
                            "collection_publication": "",
                            "soustitre_publication": subtitle,
                        }
                    )

            page_number += 1

            if test and page_number == 4:
                return self.article_data

        return self.article_data

    @log
    def articles_infos(
        self, article
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        title, date, link, subtitle = None, None, None, None

        title_tag = article.find("h2")
        if title_tag:
            title_link = title_tag.find("a")
            if title_link:
                title = title_link.get_text(strip=True).replace("\xa0", " ")
                link = title_link["href"]

        date_tag = article.find("div", class_="attribute-display_date smaller_text")
        if date_tag:
            date = self.convertir_date(date_tag.get_text(strip=True))

        subtitle_tag = article.find("div", class_="attribute-summary")
        if subtitle_tag:
            subtitle = subtitle_tag.get_text(strip=True).replace("\xa0", " ")
        else:
            subtitle = ""

        return title, date, link, subtitle

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

    @log
    def date_premiere_publication(self) -> Optional[str]:
        if not self.article_data:
            self.publications_ssmsi_dict(test=False)
        if self.article_data:
            return self.article_data[0]["date_str_publication"]
        return None
