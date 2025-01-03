import requests
from bs4 import BeautifulSoup


url = "https://dares.travail-emploi.gouv.fr/publications?page=0"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")
articles = soup.find_all("article")
for i in articles:
    print(f"VOICI : {i}")
