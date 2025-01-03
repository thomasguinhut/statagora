import subprocess
import sys
import os
import socket
from src.utils.log_init import initialiser_logs
import logging

from src.utils.log_decorator import log


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@log
def run_streamlit_app():
    try:
        # Ajouter le répertoire src au PYTHONPATH
        sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

        # Trouver un port libre
        port = find_free_port()

        # Exécuter Streamlit sans bloquer le script Python sur un port spécifique
        subprocess.Popen(["streamlit", "run", "app.py", "--server.port", str(port)])
        print(f"Streamlit est en cours d'exécution sur le port {port}.")
    except KeyboardInterrupt:
        print("L'exécution de Streamlit a été interrompue.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de Streamlit : {e}")


if __name__ == "__main__":
    run_streamlit_app()
