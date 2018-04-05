-- Generate molecule table from SMILES
SELECT  *
INTO    emolecules.mols
FROM (
    SELECT  id,
            mol_from_smiles(smiles::cstring) AS m
    FROM    raw_data
    ) AS tmp
WHERE   m IS NOT NULL
;

-- Generate molecule table from mole files
SELECT  *
INTO    rdk.mols
FROM (
    SELECT  molregno,
            mol_from_ctab(molfile::cstring) AS m
    FROM    compound_structures) tmp
    WHERE   m IS NOT NULL
;

-- Index table for structure searches
CREATE INDEX molidx
ON rdk.mols
USING gist(m)
;

-- And add a primary key
ALTER TABLE rdk.mols
ADD PRIMARY KEY (molregno)
;

--- Generate and stash fingerprints
SELECT  molregno,
        torsionbv_fp(m) AS torsionbv,
        morganbv_fp(m) AS mfp2,
        featmorganbv_fp(m) AS ffp2,
        rdkit_fp(m) AS rdkitbv,
        atompairbv_fp(m) AS atompair,
        maccs_fp(m) AS maccs
INTO rdk.fps
FROM rdk.mols
;

--- Index topological torsion fingerprints
CREATE INDEX fps_ttbv_idx
ON rdk.fps
USING gist(torsionbv)
;

--- Index Morgan (circular) fingerprints
CREATE INDEX fps_mfp2_idx
ON rdk.fps
USING gist(mfp2)
;

--- Index feature-normalizaed Morgan fingerprints
CREATE INDEX fps_ffp2_idx
ON rdk.fps
USING gist(ffp2)
;

--- Index RDKit/Daylight fingerprints (path based)
CREATE INDEX fps_rdkitbv_idx
ON rdk.fps
USING gist(rdkitbv)
;

--- Index atom-pair fingerprints
CREATE INDEX fps_atompair_idx
ON rdk.fps
USING gist(atompair)
;

--- Index MACCS (empirical flag set) fingerprints
CREATE INDEX fps_maccs_idx
ON rdk.fps
USING gist(maccs)
;
ALTER TABLE rdk.fps
ADD PRIMARY KEY (molregno)
;

--- Compute the torsion near neighbors
CREATE OR REPLACE FUNCTION get_torsionbv_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(torsionbv_fp(mol_from_smiles($1::cstring)),torsionbv) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   torsionbv_fp(mol_from_smiles($1::cstring))%torsionbv
ORDER BY    torsionbv_fp(mol_from_smiles($1::cstring))<%>torsionbv;
$$ language sql stable ;

--- Compute the Morgan near neighbors
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

--- Compute the feature morgan near neighbors
CREATE OR REPLACE FUNCTION get_ffp2_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(featmorganbv_fp(mol_from_smiles($1::cstring)),ffp2) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   featmorganbv_fp(mol_from_smiles($1::cstring))%ffp2
ORDER BY    featmorganbv_fp(mol_from_smiles($1::cstring))<%>ffp2;
$$ language sql stable ;

--- Compute the RDKit near neighbors
CREATE OR REPLACE FUNCTION get_rdkitbv_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(rdkit_fp(mol_from_smiles($1::cstring)),rdkitbv) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   rdkit_fp(mol_from_smiles($1::cstring))%rdkitbv
ORDER BY    rdkit_fp(mol_from_smiles($1::cstring))<%>rdkitbv;
$$ language sql stable ;

--- Compute the atom-pair near neighbors
CREATE OR REPLACE FUNCTION get_atompair_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(atompairbv_fp(mol_from_smiles($1::cstring)),atompair) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   atompairbv_fp(mol_from_smiles($1::cstring))%atompair
ORDER BY    atompairbv_fp(mol_from_smiles($1::cstring))<%>atompair;
$$ language sql stable ;

--- Compute the MACCS near neighbors
CREATE OR REPLACE FUNCTION get_maccs_neighbors(smiles TEXT)
RETURNS TABLE(molregno INTEGER, m mol, similarity DOUBLE PRECISION) AS
$$
SELECT  molregno,
        m,
        tanimoto_sml(maccs_fp(mol_from_smiles($1::cstring)),maccs) AS similarity
FROM    rdk.fps
    JOIN    rdk.mols USING (molregno)
WHERE   maccs_fp(mol_from_smiles($1::cstring))%maccs
ORDER BY    maccs_fp(mol_from_smiles($1::cstring))<%>maccs;
$$ language sql stable ;
