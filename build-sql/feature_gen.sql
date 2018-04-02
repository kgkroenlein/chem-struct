SELECT  *
INTO    mols
FROM (
    SELECT  id,
            mol_from_smiles(smiles::cstring) AS m
    FROM    raw_data
    ) AS tmp
WHERE   m IS NOT NULL
;

SELECT  *
INTO    rdk.mols
FROM (
    SELECT  molregno,
            mol_from_ctab(molfile::cstring) AS m
    FROM    compound_structures) tmp
    WHERE   m IS NOT NULL
;

CREATE INDEX molidx
ON rdk.mols
USING gist(m)
;

ALTER TABLE rdk.mols
ADD PRIMARY KEY (molregno)
;

SELECT  molregno,
        torsionbv_fp(m) AS torsionbv,
        morganbv_fp(m) AS mfp2,
        featmorganbv_fp(m) AS ffp2
INTO rdk.fps
FROM rdk.mols
;

CREATE INDEX fps_ttbv_idx
ON rdk.fps
USING gist(torsionbv)
;

CREATE INDEX fps_mfp2_idx
ON rdk.fps
USING gist(mfp2)
;

CREATE INDEX fps_ffp2_idx
ON rdk.fps
USING gist(ffp2)
;

ALTER TABLE rdk.fps
ADD PRIMARY KEY (molregno)
;

CREATE OR REPLACE FUNCTION get_mfp2_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(morganbv_fp(mol_from_smiles($1::cstring)),mfp2) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   morganbv_fp(mol_from_smiles($1::cstring))%mfp2
ORDER BY    morganbv_fp(mol_from_smiles($1::cstring))<%>mfp2;
$$ language sql stable ;
