-----------------------------------------------------
-- Organisme
-----------------------------------------------------
DROP TABLE IF EXISTS organisme CASCADE ;
CREATE TABLE organisme(
    id_organisme   VARCHAR PRIMARY KEY,
    nom_organisme VARCHAR NOT NULL
);