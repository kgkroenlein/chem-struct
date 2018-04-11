import numpy as np
from collections import defaultdict
from util import aws_context_db, load_data
from sklearn.ensemble import RandomForestRegressor
from rdkit.Chem import AllChem
from rdkit import DataStructs

def fp2bits(fp):
    ebv = DataStructs.cDataStructs.CreateFromBitString(fp)
    stash = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(ebv, stash)
    return stash

def predict(ctab, conn = None):
    """
    Predict the lipophilicity based upon the atom-pair nearest neighbor

    Inputs:
    ctab: {str} Character-based representation of the target structure
    conn: {psycopg2 connection} DB connection; defaults to aws_context_db()


    """
    model = load_data('app/model.pkl')
    n = 5
    if not conn:
        from util import aws_context_db
        conn = aws_context_db()
    base_cur = conn.cursor()

    default_tol_sql = 'SET rdkit.tanimoto_threshold TO DEFAULT;'
    tol_sql = 'SET rdkit.tanimoto_threshold TO %s'

    # Prepare statment is necessary because a normal psycopg2 placeholder gets
    # confused by all the percents, I think
    neighbor_sql_tmpl = '''
    PREPARE neighbor_plan AS
    SELECT  lipophilicity.value AS val,
            tanimoto_sml(target, fps.{}) AS similarity
    FROM    lipophilicity,
            rdk.fps,
            {}(mol_from_ctab($1)) AS target
    WHERE   target%fps.{}
    ORDER BY target<%>fps.{}
    LIMIT   {}
    '''

    fp_methods = {
        'mfp2': 'morganbv_fp',
        'ffp2': 'featmorganbv_fp',
        'rdkitbv': 'rdkit_fp',
        'atompair': 'atompairbv_fp',
        'torsionbv': 'torsionbv_fp',
        'maccs': 'maccs_fp',
    }

    fp_names = ('mfp2', 'ffp2', 'rdkitbv', 'atompair', 'torsionbv', 'maccs')

    fp_derived = dict()
    tmp_cur =  conn.cursor()
    tmp_cur.execute('SELECT target FROM morganbv_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['mfp2'] = fp2bits(target)
    tmp_cur.execute('SELECT target FROM featmorganbv_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['ffp2'] = fp2bits(target)
    tmp_cur.execute('SELECT target FROM rdkit_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['rdkitbv'] = fp2bits(target)
    tmp_cur.execute('SELECT target FROM atompairbv_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['atompair'] = fp2bits(target)
    tmp_cur.execute('SELECT target FROM torsionbv_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['torsionbv'] = fp2bits(target)
    tmp_cur.execute('SELECT target FROM maccs_fp(mol_from_ctab(%s)) AS target', (ctab,))
    for (target,) in tmp_cur:
        fp_derived['maccs'] = fp2bits(target)

    X = []
    highest = []
    for fp_name in fp_names:
        X += list(fp_derived[fp_name])

        tol = 0.5
        neighbor_sql = neighbor_sql_tmpl.format( fp_name,
                            fp_methods[fp_name], fp_name, fp_name, n )
        base_cur.execute(neighbor_sql)

        attempt = np.zeros([2*n,])
        while True:
            n_cur = conn.cursor()
            n_cur.execute('EXECUTE neighbor_plan (%s)', (ctab,))
            for i, (value, similarity) in enumerate(n_cur):
                attempt[2*i]   = similarity
                attempt[2*i+1] = value

            # Did we get enough?
            if attempt[-2] != 0:
                break

            # Lower the threshold and try again
            tol /= 2
            base_cur.execute(tol_sql, (tol,))

        # Reset tolerance if it changed
        if tol != 0.5:
            tol = 0.5
            base_cur.execute(default_tol_sql)

        if attempt[0] == 1:
            highest += [attempt[1]]
        X += list(attempt)
        base_cur.execute('DEALLOCATE neighbor_plan')

    pred = model.predict(np.array(X).reshape(1, -1))

    # If all fingerprints gave a sim=1, then we matched
    if len(highest) == len(fp_names):
        exp = highest[0]
    else:
        exp = None

    return pred, exp

if __name__ == '__main__':
    pass
