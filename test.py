import toml

try:
    with open("/Users/thomasguinhut/Documents/statagora/.streamlit/secrets.toml", "r") as file:
        data = toml.load(file)
    print("Le fichier TOML est valide.")
except Exception as e:
    print(f"Erreur dans le fichier TOML : {e}")
