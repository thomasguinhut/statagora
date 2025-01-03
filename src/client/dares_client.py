import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from datetime import datetime
import locale


class DaresClient:
    BASE_URL = "https://dares.travail-emploi.gouv.fr/publications"

    def __init__(self) -> None:
        self.article_data: List[dict] = []
        try:
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        except locale.Error as e:
            print(f"Erreur de paramétrage de la locale: {e}")

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
                date = date_span.get_text(strip=True).replace("\xa0", " ")
                try:
                    date_objet = datetime.strptime(date, "%d %B %Y")
                    date = date_objet.strftime("%d/%m/%Y")
                except ValueError as e:
                    print(f"Erreur de conversion de la date: {e}")

        subtitle_tag = article.find("p", class_="list-article-text")
        if subtitle_tag:
            subtitle = subtitle_tag.get_text(strip=True).replace("\xa0", " ")

        collection_tag = article.find("li", class_="list-item-alternative")
        if collection_tag:
            collection = " ".join(collection_tag.stripped_strings)

        return title, date, link, subtitle, collection

    def date_premiere_publication(self) -> Optional[str]:
        if not self.article_data:
            self.publications_dares_dict(test=False)
        if self.article_data:
            return self.article_data[0]["date_str_publication"]
        return None
