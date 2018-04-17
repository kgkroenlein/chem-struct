import numpy as np
from collections import defaultdict
from util import aws_context_db, load_data, store_data
from sklearn.ensemble import RandomForestRegressor
from rdkit import DataStructs

def fp2bits(fp):
    ebv = DataStructs.cDataStructs.CreateFromBitString(fp)
    stash = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(ebv, stash)
    return stash

def pull_all_lipo_ids(conn):
    """
    Pull all lipophilicity molregnos, sorted by molregno value

    conn: database connection

    returns list of ids
    """
    cur = conn.cursor()
    sql = '''
    SELECT  molregno
    FROM    lipophilicity
    ORDER BY molregno
    '''
    cur.execute(sql)
    return [row[0] for row in cur]

def test_train_data(conn, train_ids, test_ids, neighbors=5):
    """
    Generate neighbor lists, omitting test compounds

    conn: database connection
    train_ids: list of training compounds
    test_ids: list of test compounds

    returns X_train, X_test, y_train, y_test, where test_ids do not appear in
            X arrays
    """
    test_set = set(test_ids)
    fp_names = ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs')

    all_lipo_sql = '''
    SELECT  molregno,
            value
    FROM    lipophilicity
    '''

    neighbor_sql_tmpl = '''
    SELECT  molregno2,
            {}_sim
    FROM    fp2fp
    WHERE   molregno1 = %s
    ORDER BY {}_sim DESC
    '''

    fps_sql = '''
    SELECT  {}
    FROM    rdk.fps
    WHERE   molregno = %s
    '''.format(','.join(fp_names))

    cur = conn.cursor()

    # Gather lipophilicity data
    cur.execute(all_lipo_sql)
    lipo_dict = {k:v for (k,v) in cur}

    X_train = []
    y_train = []
    for id in train_ids:
        y_train += [lipo_dict[id]]
        row_data = []
        for fp_name in fp_names:
            cur.execute(neighbor_sql_tmpl.format(fp_name,fp_name), (id,))
            for (n_id, sim) in cur:
                if n_id in test_set:
                    continue
                row_data += [lipo_dict[n_id], sim]
                if len(row_data) % (2*neighbors) == 0:
                    break
        cur.execute(fps_sql, (id,))
        for row in cur:
            for fp in row:
                row_data += list(fp2bits(fp))

        X_train += [row_data]

    X_test = []
    y_test = []
    for id in test_ids:
        y_test += [lipo_dict[id]]
        row_data = []
        for fp_name in fp_names:
            cur.execute(neighbor_sql_tmpl.format(fp_name,fp_name), (id,))
            for (n_id, sim) in cur:
                if n_id in test_set:
                    continue
                row_data += [lipo_dict[n_id], sim]
                if len(row_data) % (2*neighbors) == 0:
                    break
        cur.execute(fps_sql, (id,))
        for row in cur:
            for fp in row:
                row_data += list(fp2bits(fp))

        X_test += [row_data]

    return np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

def all_data(conn, neighbors=5):
    """
    Generate neighbor lists for all compounds in the lipophilicity table

    conn: database connection

    returns X  neighbor similarities and lipophilicities + fingerprint for this
            y  target lipophilicity values
    """
    fp_names = ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs')

    all_lipo_sql = '''
    SELECT  molregno,
            value
    FROM    lipophilicity
    '''

    neighbor_sql_tmpl = '''
    SELECT  molregno2,
            {}_sim
    FROM    fp2fp
    WHERE   molregno1 = %s
    ORDER BY {}_sim DESC
    '''

    fps_sql = '''
    SELECT  {}
    FROM    rdk.fps
    WHERE   molregno = %s
    '''.format(','.join(fp_names))

    cur = conn.cursor()

    # Gather lipophilicity data
    cur.execute(all_lipo_sql)
    lipo_dict = {k:v for (k,v) in cur}

    X = []
    y = []
    for id in train_ids:
        y += [lipo_dict[id]]
        row_data = []
        for fp_name in fp_names:
            cur.execute(neighbor_sql_tmpl.format(fp_name,fp_name), (id,))
            for (n_id, sim) in cur:
                row_data += [lipo_dict[n_id], sim]
                if len(row_data) % (2*neighbors) == 0:
                    break
        cur.execute(fps_sql, (id,))
        for row in cur:
            for fp in row:
                row_data += list(fp2bits(fp))

        X += [row_data]

    return np.array(X),np.array(y)

def validate(n_shuffle = 5, k_folds = 5, noisy=False):
    '''
    Validate the model via multiple shuffles and folds

    n_shuffle: {int}  Number of shuffles to perform
    k_folds: {int}  Number of folds to perform
    noisy: {bool}  controls output level
    '''
    conn = aws_context_db()
    indices = pull_all_lipo_ids(conn)

    seed(56)
    for i_shuffle in range(n_shuffle):
        if noisy:
            print(i_shuffle, datetime.now().time())
        shuffle(indices)
        for k in range(k_folds):
            if noisy:
                print(k, datetime.now().time())
            num_idx = len(indices)
            train_idx = [i for i in indices[0:(k*num_idx)//k_folds]]           \
                       +[i for i in indices[((k+1)*num_idx)//k_folds:num_idx]]
            test_idx = [i for i in indices[(k*num_idx)//k_folds:((k+1)*num_idx)//k_folds]]

            X_train, X_test, y_train, y_test = \
                test_train_data(conn, train_idx, test_idx)

            rf = RandomForestRegressor(n_estimators = 1000, max_depth=10, n_jobs = -1)
            rf.fit(X_train, y_train)
            if noisy:
                print('Train R2: ', rf.score(X_train, y_train))
                print('    RMSE: ', sqrt(mean_squared_error(y_train, rf.predict(X_train))))

            print('Test  R2: ', rf.score(X_test,y_test))
            print('    RMSE: ', sqrt(mean_squared_error(y_test, rf.predict(X_test))))

def predict(ctab, neighbors=5, conn = None):
    """
    Predict the lipophilicity based upon the atom-pair nearest neighbor

    Inputs:
    ctab: {str} Character-based representation of the target structure
    conn: {psycopg2 connection} DB connection; defaults to aws_context_db()


    """
    model = load_data('lipo_model.pkl')

    if not conn:
        from util import aws_context_db
        conn = aws_context_db()
    cur = conn.cursor()

    # Compute the fingerprints
    fp_names = ('mfp2', 'ffp2', 'rdkitbv', 'atompair', 'torsionbv', 'maccs')
    fp_sql = '''
    SELECT  morganbv_fp(m) AS mfp2,
            featmorganbv_fp(m) AS ffp2,
            rdkit_fp(m) AS rdkitbv,
            atompairbv_fp(m) AS atompair,
            torsionbv_fp(m) AS torsionbv,
            maccs_fp(m) AS maccs
    FROM    mol_from_ctab(%s) AS m
    '''
    fp_dict = dict()
    cur.execute(fp_sql, (ctab,))
    for row in cur:
        fp_dict = {fp_names[i]:row[i] for i in range(len(fp_names))}

    cur.execute('''
    SELECT  lipophilicity.molregno AS regno,
            lipophilicity.value AS val
    FROM    lipophilicity,
            rdk.fps
    WHERE   lipophilicity.molregno=rdk.fps.molregno
      AND   fps.mfp2 = %s
      AND   fps.ffp2 = %s
      AND   fps.rdkitbv = %s
      AND   fps.atompair = %s
      AND   fps.torsionbv = %s
      AND   fps.maccs = %s
    ''', (fp_dict['mfp2'],fp_dict['ffp2'],fp_dict['rdkitbv'],
            fp_dict['atompair'],fp_dict['torsionbv'],fp_dict['maccs'],))

    exact_no = None
    exp = None
    for row in cur:
        exact_no = row[0]
        exp = row[1]

    default_tol_sql = 'SET rdkit.tanimoto_threshold TO DEFAULT;'
    tol_sql = 'SET rdkit.tanimoto_threshold TO %s'

    X = []
    if exact_no: # Easy, we got a perfect match (probably)
        neighbor_sql_tmpl = '''
        SELECT  lipophilicity.value AS val,
                {}_sim
        FROM    fp2fp,
                lipophilicity
        WHERE   molregno1 = %s
          AND   molregno2 = lipophilicity.molregno
        ORDER BY {}_sim DESC
        LIMIT   {}
        '''
        for fp_name in fp_names:
            neighbor_sql = neighbor_sql_tmpl.format(fp_name,fp_name,neighbors)
            cur.execute(neighbor_sql,(exact_no,))
            for row in cur:
                X += row
                if len(X) % (2*neighbors) == 0:
                    break
        for fp_name in fp_names:
            row_data += list(fp2bits(fp_dict[fp_name]))

    else: # Gotta search 'em all
        # Grab near neighbors, with multiple levels of escaping going on
        neighbor_sql_tmpl = '''
        SELECT  lipophilicity.value AS val,
                tanimoto_sml(%s, fps.{}) AS similarity
        FROM    lipophilicity,
                rdk.fps,
        WHERE   %s %% fps.{}
          AND   lipophilicity.molregno = fps.molregno
        ORDER BY %s <%%> fps.{}
        LIMIT   {}
        '''

        for fp_name in fp_names:
            tol = 0.5
            neighbor_sql = neighbor_sql_tmpl.format( (fp_name,)*3, neighbors )

            attempt = np.zeros([2*neighbors,])
            while True:
                cur.execute(neighbor_sql, (fp_dict[fp_name],)*3)
                for i, (value, similarity) in enumerate(n_cur):
                    attempt[2*i]   = similarity
                    attempt[2*i+1] = value

                # Did we get enough?
                if attempt[-2] != 0:
                    break

                # Lower the threshold and try again
                tol /= 2
                cur.execute(tol_sql, (tol,))

            # Reset tolerance if it changed
            if tol != 0.5:
                tol = 0.5
                cur.execute(default_tol_sql)

            X += list(attempt)

        for fp_name in fp_names:
            X += list(fp2bits(fp_dict[fp_name]))

    pred = model.predict(np.array(X).reshape(1, -1))

    return pred, exp

if __name__ == '__main__':
    conn = aws_context_db()
    X, y = all_data(conn)
    rf = RandomForestRegressor(n_estimators = 1000, max_depth=10, n_jobs = -1)
    rf.fit(X_train, y_train)
    store_data(rf, 'lipo_model.pkl')
