import logging

from log_decorator import log
from singleton import Singleton
from dao.db_connection import bdd


class ResetDatabase(metaclass=Singleton):
    """

    Initialisation de la vraie base de données.

    """

    @log
    def reset(self):
        return bdd("ecrire", "publications")


if __name__ == "__main__":
    ResetDatabase().reset()
