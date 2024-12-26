-----------------------------------------------------
-- Organisme
-----------------------------------------------------
DROP TABLE IF EXISTS organisme CASCADE;
CREATE TABLE organisme(
    nom_organisme VARCHAR PRIMARY KEY,
    logo BYTEA
);

-----------------------------------------------------
-- Publication
-----------------------------------------------------
DROP TABLE IF EXISTS publication CASCADE;
CREATE TABLE publication(
    titre_publication VARCHAR PRIMARY KEY,
    date_publication VARCHAR NOT NULL,
    lien_publication VARCHAR NOT NULL,
    organisme_publication VARCHAR NOT NULL,
    soustitre_publication VARCHAR NOT NULL,
    collection_publication VARCHAR NOT NULL,
    FOREIGN KEY (organisme_publication) REFERENCES organisme(nom_organisme)
);

-- Exemple d'insertion d'un organisme
INSERT INTO organisme (nom_organisme) VALUES
('dares')
