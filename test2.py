from src.dao.db_connection import DBConnection
from src.dao.reset_database import ResetDatabase
from src.client.ssmsi_client import SsmsiClient
from src.client.dares_client import DaresClient
from src.service.publication_service import PublicationService

print(ResetDatabase().doit_reset())
