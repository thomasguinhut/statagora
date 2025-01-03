import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


class DBConnection:

    def connection(self):
        # Définition des scopes pour l'API Google Sheets
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        # Lecture des credentials depuis secrets.toml
        credentials_info = {
            "type": st.secrets["connections"]["gsheets"]["type"],
            "project_id": st.secrets["connections"]["gsheets"]["project_id"],
            "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
            "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["connections"]["gsheets"]["client_email"],
            "client_id": st.secrets["connections"]["gsheets"]["client_id"],
            "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
            "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"][
                "auth_provider_x509_cert_url"
            ],
            "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"],
        }

        # Initialisation de l'objet d'autorisation
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
        gc = gspread.authorize(credentials)

        # Ouverture du fichier Google Sheets
        sheet = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
        sheet_info = sheet.worksheet("publications")

        return sheet_info

    def afficher_df(self) -> pd.DataFrame:
        sheet_info = self.connection("publications")
        records = sheet_info.get_all_records()
        df = pd.DataFrame(records)
        return df
