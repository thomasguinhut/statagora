from dao.organisme_dao import OrganismeDao

from utils.log_decorator import log


class OrganismeService:

    @log
    def creer(self, organisme):
        if OrganismeDao().creer(organisme):
            return True
        else:
            return None
