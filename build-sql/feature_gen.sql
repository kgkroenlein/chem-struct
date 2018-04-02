SELECT  *
INTO    mols
FROM (
    SELECT  id,
            mol_from_smiles(smiles::cstring) AS m
    FROM    raw_data
    ) AS tmp
WHERE   m IS NOT NULL
;
