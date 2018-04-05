-- Schemas and extensions
CREATE EXTENSION rdkit;
CREATE SCHEMA chemstruct;
CREATE SCHEMA emolecules;
CREATE SCHEMA chembl;
CREATE SCHEMA rdk;

ALTER ROLE postgres
SET search_path
TO chemstruct, emolecules, chembl, rdk, public;

-- Store raw data from emolecules
-- https://www.emolecules.com/info/plus/download-database
CREATE TABLE emolecules.raw_data (
    id      SERIAL,
    smiles  TEXT,
    emol_id INTEGER,
    parent_id INTEGER
);

-- Data from Delaney DOI: 10.1021/ci034243x
CREATE TABLE chemstruct.solubility (
    cmp_name VARCHAR(100)       NOT NULL,
    predict  DOUBLE PRECISION   NOT NULL,
    mindeg   INTEGER            NOT NULL,
    mmass    DOUBLE PRECISION   NOT NULL,
    hbond    INTEGER            NOT NULL,
    rings    INTEGER            NOT NULL,
    rotbond  INTEGER            NOT NULL,
    surfarea DOUBLE PRECISION   NOT NULL,
    measure  DOUBLE PRECISION   NOT NULL,
    smiles   VARCHAR(200)       PRIMARY KEY
);
