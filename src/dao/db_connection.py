import gspread
from oauth2client.service_account import ServiceAccountCredentials


class DBConnection:

    def connection(self):

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

        return sheet
