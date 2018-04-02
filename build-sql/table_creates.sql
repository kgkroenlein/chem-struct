CREATE EXTENSION rdkit;

CREATE TABLE raw_data (
    id SERIAL,
    smiles TEXT,
    emol_id INTEGER,
    parent_id INTEGER
);
