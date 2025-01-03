from datetime import datetime


def convertir_date(date_str):
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


date = "2 mai 2024"
date_convertie = convertir_date(date)
print(date_convertie)
