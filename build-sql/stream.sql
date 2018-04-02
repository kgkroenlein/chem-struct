COPY raw_data (
    smiles,
    emol_id,
    parent_id
)
FROM    stdin WITH DELIMITER ' '
