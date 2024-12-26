import subprocess


def run_streamlit_app():
    try:
        # Exécuter Streamlit sans bloquer le script Python
        subprocess.Popen(["streamlit", "run", "src/app.py"])
        print("Streamlit est en cours d'exécution.")
    except KeyboardInterrupt:
        print("L'exécution de Streamlit a été interrompue.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de Streamlit : {e}")


if __name__ == "__main__":
    run_streamlit_app()
