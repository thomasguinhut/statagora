import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from datetime import datetime


class InseeBlogClient:
    BASE_URL = "https://blog.insee.fr"

    def __init__(self) -> None:
        self.article_data: List[dict] = []

    def publications_insee_blog(self, page_number: int) -> Optional[BeautifulSoup]:
        url = f"{self.BASE_URL}/page/{page_number}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an error for 4xx/5xx status codes
        except requests.RequestException as e:
            print(f"Erreur lors de la requête HTTP: {e}")
            return None

        return BeautifulSoup(response.content, "html.parser")

    def publications_insee_blog_dict(self, test: bool = False) -> List[dict]:
        page_number = 1
        empty_pages = 0

        while True:
            soup = self.publications_insee_blog(page_number)
            if not soup:
                empty_pages += 1
                print(
                    f"Page {page_number} vide ou inaccessible. Compteur de pages vides : {empty_pages}"
                )
                if empty_pages >= 2:
                    print("Fin des pages après 2 pages vides consécutives.")
                    break
            else:
                empty_pages = 0

            articles = soup.find_all("div", class_="blog-paralle") if soup else []
            if not articles:
                empty_pages += 1
                if empty_pages >= 2:
                    break
            else:
                empty_pages = 0

            for article in articles:
                title, date, link, excerpt = self.articles_infos(article)
                if title or date or link or excerpt:
                    self.article_data.append(
                        {
                            "titre_publication": title,
                            "date_str_publication": date,
                            "lien_publication": link,
                            "id_organisme_publication": "insee_blog",
                            "soustitre_publication": excerpt,
                            "collection_publication": "",
                        }
                    )

            page_number += 1

            if test and page_number == 3:
                return self.article_data

        return self.article_data

    def articles_infos(
        self, article
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
        title, date, link, excerpt = None, None, None, None

        # Title and link
        title_tag = article.find("h3", class_="entry-title")
        if title_tag:
            link_tag = title_tag.find("a")
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = link_tag["href"]

        # Date
        date_tag = article.find("span", class_="post-date")
        if date_tag:
            date_link = date_tag.find("a")
            if date_link:
                date = self.convertir_date(date_link.get_text(strip=True))

        # Excerpt
        excerpt_tag = article.find("p")
        if excerpt_tag:
            excerpt = excerpt_tag.get_text(strip=True)

        return title, date, link, excerpt

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
