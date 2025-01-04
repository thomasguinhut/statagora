import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from datetime import datetime


class DreesClient:
    BASE_URL = "https://drees.solidarites-sante.gouv.fr/recherche?f%5B0%5D=content_type%3A1&f%5B1%5D=content_type%3A2&f%5B2%5D=content_type%3A4&f%5B3%5D=content_type%3A506"

    def __init__(self) -> None:
        self.article_data: List[dict] = []

    def publications_drees(self, page_number: int) -> List[BeautifulSoup]:
        url = f"{self.BASE_URL}/?page={page_number}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête HTTP: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("li", class_="search-result-item")
        return articles

    def publications_drees_dict(self, test: bool = False) -> List[dict]:
        page_number = 0
        empty_pages = 0

        while True:
            articles = self.publications_drees(page_number)

            if not articles:
                empty_pages += 1
                print(f"Page {page_number} vide. Compteur de pages vides : {empty_pages}")
                if empty_pages >= 2:
                    print("Fin des pages après 2 pages vides consécutives.")
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
                            "lien_publication": link,
                            "id_organisme_publication": "drees",
                            "soustitre_publication": subtitle,
                            "collection_publication": collection,
                        }
                    )

            page_number += 1

            if test and page_number == 2:
                return self.article_data

        return self.article_data

    def articles_infos(
        self, article
    ) -> Tuple[
        Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        title, link, date, subtitle, collection = None, None, None, None, None

        # Extract title and link
        title_tag = article.find("h3", class_="search-result-item--title")
        if title_tag:
            link_tag = title_tag.find("a")
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = f"{self.BASE_URL}{link_tag['href']}"

        # Extract date
        date_tag = article.find("li", class_="search-result-item--information--date")
        if date_tag:
            time_tag = date_tag.find("time")
            if time_tag:
                date = time_tag.get_text(strip=True)

        # Extract subtitle
        subtitle_tag = article.find("div", class_="field--name-field-search-result-chapo")
        if subtitle_tag:
            subtitle = subtitle_tag.get_text(strip=True)

        # Extract collection
        collection_tag = article.find("ul", class_="search-result-item--collection")
        if collection_tag:
            collection = " | ".join(
                item.get_text(strip=True) for item in collection_tag.find_all("li")
            )

        return title, date, link, subtitle, collection

    def convertir_date(self, date_str):
        # Assume input format is DD/MM/YYYY
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%d")  # Return as YYYY-MM-DD
        except ValueError:
            print(f"Erreur lors de la conversion de la date : {date_str}")
            return None
