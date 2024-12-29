import subprocess
import sys
import os


def run_streamlit_app():
    try:
        # Ajouter le répertoire src au PYTHONPATH
        sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

        # Exécuter Streamlit sans bloquer le script Python
        subprocess.Popen(["streamlit", "run", "app.py"])
        print("Streamlit est en cours d'exécution.")
    except KeyboardInterrupt:
        print("L'exécution de Streamlit a été interrompue.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de Streamlit : {e}")


if __name__ == "__main__":
    run_streamlit_app()
