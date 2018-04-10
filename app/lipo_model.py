import numpy as np
from collections import defaultdict

def predict(ctab, conn = None):
    """
    Predict the lipophilicity based upon the atom-pair nearest neighbor

    Inputs:
    ctab: {str} Character-based representation of the target structure
    conn: {psycopg2 connection} DB connection; defaults to aws_context_db()


    """
    if not conn:
        from util import aws_context_db
        conn = aws_context_db()

    sql = '''
    SELECT  lipophilicity.value AS val,
            tanimoto_sml( ap, fps.atompair ) AS similarity
    FROM    lipophilicity,
            rdk.fps,
            morganbv_fp(mol_from_ctab(%s)) AS ap
            tanimoto_sml( f1.atompair, f2.atompair ) AS similarity
    WHERE   ap % fps.atompair
      AND   lipophilicity.molregno = fps.molregno
    ORDER BY ap<%>fps.atompair
    LIMIT 30
    '''

    cur = conn.cursor()
    cur.execute('SET rdkit.tanimoto_threshold TO 0.2')
    cur.execute(sql,(ctab,))
    exp = None
    norm = 0
    summ = 0
    for (val,similarity) in cur:
        if similarity == 1:
            exp = val # There's a true answer in there
        else:
            weight = np.exp(25.0*similarity)
            norm += weight
            summ += val*weight
    if norm == 0:
        pred = None
    else:
        pred = summ/norm

    return pred, exp

if __name__ == '__main__':
    pass
