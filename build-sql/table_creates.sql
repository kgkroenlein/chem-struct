CREATE EXTENSION rdkit;
CREATE SCHEMA emolecules;
CREATE SCHEMA chembl;
CREATE SCHEMA rdk;
ALTER ROLE postgres SET search_path TO emolecules, chembl, rdk, public;
CREATE TABLE emolecules.raw_data (
    id SERIAL,
    smiles TEXT,
    emol_id INTEGER,
    parent_id INTEGER
);
