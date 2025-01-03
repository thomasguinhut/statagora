import os
import logging
import logging.config
import yaml


def initialiser_logs(nom):
    """Initialiser les logs à partir du fichier de config"""

    # Affiche le répertoire de travail actuel
    print(os.getcwd())

    # Change le répertoire de travail
    os.chdir("/Users/thomasguinhut/Documents/statagora")

    # Création du dossier logs à la racine si non existant
    os.makedirs("logs", exist_ok=True)

    # Ouverture et chargement du fichier de configuration YAML
    with open("logging_config.yml", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # Configuration du logging à partir du dictionnaire de configuration
    logging.config.dictConfig(config)

    # Ajout d'entrées de log pour indiquer le lancement
    logging.info("-" * 50)
    logging.info(f"Lancement {nom}                           ")
    logging.info("-" * 50)


# Exemple d'utilisation
initialiser_logs("MonApplication")
