-----------------------------------------------------
-- Organisme
-----------------------------------------------------
DROP TABLE IF EXISTS organisme CASCADE;
CREATE TABLE organisme(
    nom_organisme VARCHAR PRIMARY KEY,
    nom_explicite_organisme VARCHAR NOT NULL
);

-----------------------------------------------------
-- Publication
-----------------------------------------------------
DROP TABLE IF EXISTS publication CASCADE;
CREATE TABLE publication(
    titre_publication VARCHAR PRIMARY KEY,
    date_publication DATE NOT NULL,
    lien_publication VARCHAR NOT NULL,
    organisme_publication VARCHAR NOT NULL,
    soustitre_publication VARCHAR NOT NULL,
    collection_publication VARCHAR NOT NULL,
    FOREIGN KEY (organisme_publication) REFERENCES organisme(nom_organisme)
);

INSERT INTO organisme (nom_organisme, nom_explicite_organisme) VALUES
('dares', 'Dares'),
('insee', 'Insee'),
('ssmsi', 'SSMSI')
