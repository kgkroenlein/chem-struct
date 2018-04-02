CREATE EXTENSION rdkit;
CREATE SCHEMA emolecules;
CREATE SCHEMA chembl;
ALTER USER user_name SET search_path TO 'emolecules, chembl, ', || current_setting('search_path');
CREATE TABLE emolecules.raw_data (
    id SERIAL,
    smiles TEXT,
    emol_id INTEGER,
    parent_id INTEGER
);
