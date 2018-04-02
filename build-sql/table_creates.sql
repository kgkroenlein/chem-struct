CREATE EXTENSION rdkit;
CREATE SCHEMA emolecules;
CREATE SCHEMA chembl;
SELECT set_config(
    'search_path',
    'emolecules, ' || current_setting('search_path'),
    false
) WHERE current_setting('search_path') !~ '(^|\W)emolecules($|\W)';
SELECT set_config(
    'search_path',
    'chembl, ' || current_setting('search_path'),
    false
) WHERE current_setting('search_path') !~ '(^|\W)chembl($|\W)';
ALTER ROLE postgres SET search_path TO current_setting('search_path');
CREATE TABLE emolecules.raw_data (
    id SERIAL,
    smiles TEXT,
    emol_id INTEGER,
    parent_id INTEGER
);
