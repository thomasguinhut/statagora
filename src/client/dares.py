import locale
import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime


class DaresClient:
    def __init__(self) -> None:
        pass

    def get_all_dares(self) -> List[dict]:
        article_data = []
        page_number = 0  # Numéro de la page à parcourir
        empty_pages = 0  # Compteur de pages vides consécutives

        for i in range(2):
            url = f"https://dares.travail-emploi.gouv.fr/publications?page={
                page_number}"

            # Envoyer une requête GET à l'URL
            response = requests.get(url)
            if response.status_code != 200:
                print(
                    f"Erreur lors de la récupération de la page {
                        page_number}: {response.status_code}"
                )
                break  # Arrêter en cas d'erreur critique

            # Analyser le contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trouver tous les articles (balise <article>)
            articles = soup.find_all('article')

            # Vérifier si la page est vide
            if not articles:
                empty_pages += 1
                print(
                    f"Page {page_number} vide. Compteur de pages vides : {
                        empty_pages}"
                )
                if empty_pages >= 2:
                    print(
                        f"Fin des pages après {
                            empty_pages} pages vides consécutives."
                    )
                    break
            else:
                empty_pages = 0  # Réinitialiser le compteur si une page contient des articles

            for article in articles:
                # Initialiser des variables par défaut
                title = None
                date = None
                link = None
                subtitle = None
                collection = None  # Nouvelle clé pour la collection

                # Extraire le titre
                title_tag = article.find('h3', class_='list-article-title')
                if title_tag:
                    title_link = title_tag.find('a')
                    if title_link:
                        title = title_link.get_text(
                            strip=True).replace('\xa0', ' ')
                        link = title_link['href']

                # Extraire la date
                date_tag = article.find(
                    'ul', class_='list-article-information')
                if date_tag:
                    date_span = date_tag.find(
                        'li', class_='list-item').find('span')
                    if date_span:
                        date = date_span.get_text(
                            strip=True).replace('\xa0', ' ')

                # Extraire le sous-titre
                subtitle_tag = article.find('p', class_='list-article-text')
                if subtitle_tag:
                    subtitle = subtitle_tag.get_text(
                        strip=True).replace('\xa0', ' ')

                # Extraire la collection
                collection_tag = article.find(
                    'li', class_='list-item-alternative')
                if collection_tag:
                    # Récupère tout le texte dans l'élément
                    collection = ' '.join(collection_tag.stripped_strings)

                # Configurer la locale pour interpréter la date en français
                try:
                    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
                except locale.Error:
                    # Windows fallback
                    locale.setlocale(locale.LC_TIME, 'French_France.1252')

                # Convertir et formater la date
                try:
                    if date:
                        date_objet = datetime.strptime(date, "%d %B %Y")
                        date_formatee = date_objet.strftime("%d/%m/%Y")
                    else:
                        date_formatee = "Non spécifiée"
                except ValueError:
                    date_formatee = "Erreur de conversion"

                # Filtrer les articles vides
                if title or date or link or subtitle or collection:
                    article_data.append({
                        'title': title,
                        'date': date_formatee,
                        'link': f"https://dares.travail-emploi.gouv.fr{link}" if link else None,
                        'organisme': "dares",
                        'subtitle': subtitle,
                        'collection': collection  # Ajout de la collection au dictionnaire
                    })

            # Passer à la page suivante
            page_number += 1

        return article_data


if __name__ == "__main__":
    client = DaresClient()
    results = client.get_all_dares()
    for article in results:
        print(article['title'])
