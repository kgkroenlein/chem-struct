import psycopg2
from collections import defaultdict

from util import store_data, load_data

def gather_near_neighbors(n = 15, conn = None, output=False
          fps = ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs')):
    """Example function with types documented in the docstring.

    Args:
        n      (int): The number of nearest neighbors to include; default 10.
                      Default chosen as likely to have all 4200 compounds able
                      to drop a 20 % test set and still include 5 neighbors in
                      all fingerprints (~.1% chance of problem)
        conn   (db) : The connector to the db of interest; defaults to None,
                      in which case util.aws_context_db() is invoked.
        fps (list(str)): The fingerprints to generate lists for

    Returns:
        dict(dict(dict)): The mapped neighborhood, keyed as return[fp][id1]

    """
    if int(n) != n or n <= 0:
        raise ValueError('Invalid list length passed')
    known_fps = {'mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'}
    if len(fps) == 0:
        raise ValueError('Empty fingerprint list passed')
    for fp in fps:
        if fp not in known_fps:
            raise ValueError('Unrecognized fingerprint type: ', fp)

    if not conn:
        from util import aws_context_db
        conn = aws_context_db()

    compound_sql = '''
    SELECT  molregno
    FROM    lipophilicity
    '''

    default_tol_sql = 'SET rdkit.tanimoto_threshold TO DEFAULT;'
    tol_sql = 'SET rdkit.tanimoto_threshold TO %s'

    neighbor_sql_tmpl = '''
    PREPARE neighbor_plan
    SELECT  fp2.molregno AS molregno,
            tanimoto_sml(fp1.{}, fp2.{}) AS similarity
    FROM    lipophilicity t2,
            rdk.fps fp1,
            rdk.fps fp2
    WHERE   fp1.molregno = $1
      AND   fp2.molregno = t2.molregno
      AND   fp1.{}%fp2.{}
    ORDER BY fp1.{}<%>fp2.{}
    LIMIT   {}
    '''

    result = defaultdict(lambda: defaultdict(dict))
    for fp_name in fps:
        if output:
            print('Starting ', fp_name)

        base_cur = conn.cursor() # Reused cursor
        base_cur.execute(neighbor_sql_tmpl.format( *(fp_name)*6, n ))

        cmp_cur = conn.cursor() # Cursor for getting compound list
        cur.execute(compound_sql.format(fp_name))
        tol = 0.5
        for i, (id,) in enumerate(cmp_cur):
            if output and i % 100 == 0:
                print('Compound {:4.0f}:{}'.format(i,id))
            while True:
                n_cur = conn.cursor()
                n_cur.execute('EXECUTE neighbor_plan (%s)', (id,))
                for (n_id, similarity) in n_cur:
                    result[fp_name][id][n_id] = similarity

                # Did we get enough?
                if len(result[fp_name][id] >= n):
                    break

                # Lower the threshold and try again
                tol /= 2
                base_cur.execute(tol_sql, (tol,))

            # Reset tolerance if it changed
            if tol != 0.5:
                tol = 0.5
                base_cur.execute(default_tol_sql)

    return result

if __name__ == '__main__':
    data = gather_near_neighbors(output=True)
    store_data(data, 'nmap.pkl')
