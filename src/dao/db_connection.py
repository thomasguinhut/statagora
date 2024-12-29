import gspread
from oauth2client.service_account import ServiceAccountCredentials
from client.dares_client import DaresClient
import pandas as pd
import traceback


def bdd(action, feuille=None):
    # Vérification des paramètres
    if action not in ["lire", "ecrire"]:
        raise ValueError("L'action sur la feuille est mal spécifiée.")
    if feuille not in ["publications", "organismes"]:
        raise ValueError("Le nom de la feuille est mal spécifié.")

    # Détermination de l'index de la feuille
    index_feuille = 0 if feuille == "publications" else 1

    # Définition des scopes pour l'API Google Sheets
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    # Lecture des credentials depuis le fichier JSON
    credentials = ServiceAccountCredentials.from_json_keyfile_name("data/statagora.json", scope)

    # Initialisation de l'objet d'autorisation
    gc = gspread.authorize(credentials)

    # Ouverture du fichier Google Sheets
    sheet = gc.open("statagora_base")

    if action == "lire":
        try:
            # Lecture des données de la feuille
            sheet_info = sheet.get_worksheet(index_feuille)
            records = sheet_info.get_all_records()
            df = pd.DataFrame(records)
            return df
        except gspread.exceptions.GSpreadException as e:
            print(f"Erreur lors de la lecture de la feuille: {e}")
            return pd.DataFrame()
    else:
        try:
            # Écriture des données dans la feuille
            r = DaresClient().get_all_dares(True)
            df = pd.DataFrame(r)
            worksheet = sheet.get_worksheet(index_feuille)
            test = [df.columns.values.tolist()] + df.values.tolist()
            worksheet.update(
                values=[df.columns.values.tolist()] + df.values.tolist(), range_name="A1"
            )
        except gspread.exceptions.GSpreadException as e:
            print(f"Erreur lors de l'écriture dans la feuille: {e}")
        except Exception as e:
            print(f"Erreur inattendue: {traceback.format_exc()}")
        return


# Appel de la fonction
if __name__ == "__main__":
    print(bdd("lire", "publications"))
