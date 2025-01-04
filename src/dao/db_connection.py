import streamlit as st
import pandas as pd
import logging
import os

from src.utils.log_decorator import log


class DBConnection:

    @log
    def afficher_feuille(self, id_organisme):
        dossier_courant = os.path.abspath(os.path.dirname(__file__))
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.join(dossier_courant, "data")
        df = os.path.join(dossier_courant, f"publications_{id_organisme}.csv")
        return pd.read_csv(df)

    @log
    def enregistrer_feuille(self, df, id_organisme):
        dossier_courant = os.path.abspath(os.path.dirname(__file__))
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.join(dossier_courant, "data")
        dossier_courant = os.path.join(dossier_courant, f"publications_{id_organisme}.csv")
        df.to_csv(dossier_courant, index=False)

    @log
    def supprimer_feuille(self, id_organisme):
        dossier_courant = os.path.abspath(os.path.dirname(__file__))
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.dirname(dossier_courant)
        dossier_courant = os.path.join(dossier_courant, "data")
        dossier_courant = os.path.join(dossier_courant, f"publications_{id_organisme}.csv")
        os.remove(dossier_courant)

    @log
    def afficher_df(self) -> pd.DataFrame:
        df_dares = self.afficher_feuille("dares")
        df_ssmsi = self.afficher_feuille("ssmsi")

        df = pd.concat([df_dares, df_ssmsi], ignore_index=True)

        if not df.empty and "date_publication" in df.columns:
            df["date_publication"] = pd.to_datetime(df["date_publication"])
            df = df.sort_values(by="date_publication", ascending=False)

        return df
