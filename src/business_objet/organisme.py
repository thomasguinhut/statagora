import logging
from src.utils.log_decorator import log


class Organisme:

    @log
    def __init__(self, id_organisme=None, nom_officiel_organisme=None):
        self.id_organisme = id_organisme
        self.nom_officiel_organisme = nom_officiel_organisme

    @log
    def get_nom_officiel_organisme(self, id_organisme: str) -> str:
        if id_organisme == "dares":
            return "Dares"
        elif id_organisme == "insee":
            return "Insee"
        elif id_organisme == "ssmsi":
            return "SSM-SI"

    @log
    def get_id_organisme(self, nom_officiel: str) -> str:
        if nom_officiel == "Dares":
            return "dares"
        elif nom_officiel == "Insee":
            return "insee"
        elif nom_officiel == "SSM-SI":
            return "ssmsi"
        else:
            return None
