import logging
from dao.db_connection import DBConnection
import pandas as pd


class PublicationDao:

    def afficher_publications(self):
        sheet = DBConnection().connection()
        sheet_info = sheet.worksheet("publications")
        records = sheet_info.get_all_records()
        df = pd.DataFrame(records)
        return df

    def afficher_date_la_plus_récente_base(self, id_organisme):
        df = self.afficher_publications()
        df = df[df["id_organisme_publication"] == id_organisme]
        return df["date_publication"].max() if not df.empty else None
