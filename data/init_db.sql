-----------------------------------------------------
-- Organisme
-----------------------------------------------------
DROP TABLE IF EXISTS organisme CASCADE ;
CREATE TABLE organisme(
    id_organisme   VARCHAR PRIMARY KEY,
    nom_organisme VARCHAR NOT NULL UNIQUE
);

-----------------------------------------------------
-- Publication
-----------------------------------------------------
DROP TABLE IF EXISTS publication CASCADE ;
CREATE TABLE publication(
    id_publication VARCHAR PRIMARY KEY,
    titre_publication VARCHAR NOT NULL,
    date_publication VARCHAR NOT NULL,
    lien_publication VARCHAR NOT NULL,
    organisme_publication VARCHAR NOT NULL,
    soustitre_publication VARCHAR NOT NULL,
    collection_publication VARCHAR NOT NULL,
    FOREIGN KEY (organisme_publication) REFERENCES organisme(nom_organisme)
);

INSERT INTO organisme (id_organisme, nom_organisme) VALUES
('1', 'dares')