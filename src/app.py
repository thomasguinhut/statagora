import streamlit as st

# Connexion à la base de données PostgreSQL
conn = st.connection("postgresql", type="sql")

# Requête SQL pour récupérer les publications et les logos
query = """
SELECT *
FROM 
    statagora.publication;
"""

# Exécution de la requête sans cache
df = conn.query(query)

# Affichage des publications sous forme de liste à puces avec image et texte côte à côte
for row in df.itertuples():
    # Créer deux colonnes : une pour l'image et une pour le texte
    col1, col2 = st.columns(
        [1, 4]
    )  # La première colonne pour l'image, plus petite, et la deuxième pour le texte

    # Dans la première colonne, afficher l'image sans redimensionner
    with col1:
        image_path = (
            f"/Users/thomasguinhut/Documents/statagora/data/logos/{row.organisme_publication}.png"
        )
        try:
            # Affichage de l'image dans sa taille d'origine (pas de redimensionnement)
            st.image(image_path)
        except Exception as e:
            st.warning(f"Image non trouvée pour {row.organisme_publication} : {e}")

    # Dans la deuxième colonne, afficher le texte
    with col2:
        st.markdown(
            f"**[{row.titre_publication}]({row.lien_publication})** - "
            f"**{row.date_publication}** - *{row.collection_publication}*"
        )
        st.markdown(f"{row.soustitre_publication}")
        st.markdown("---")
