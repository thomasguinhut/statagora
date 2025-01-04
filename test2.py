from src.dao.db_connection import DBConnection
from src.dao.reset_database import ResetDatabase
from src.client.ssmsi_client import SsmsiClient
from src.client.dares_client import DaresClient

df = DBConnection().afficher_df()
ResetDatabase().reset_publications(df, True)
# ResetDatabase().trier_publications(df)

"""articles = SsmsiClient().publications_ssmsi_dict(True)
t = 1
for i in articles:
    print(f"{t} : {type(i["soustitre_publication"])}")
    t += 1
"""
