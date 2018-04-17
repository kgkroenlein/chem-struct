import numpy as np
from collections import defaultdict
from util import aws_context_db
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from rdkit import DataStructs
from datetime import datetime
from numpy.random import shuffle, seed

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

def test_train_data(conn, train_ids, test_ids):
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
                if len(row_data) % 10 == 0:
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
                if len(row_data) % 10 == 0:
                    break
        cur.execute(fps_sql, (id,))
        for row in cur:
            for fp in row:
                row_data += list(fp2bits(fp))

        X_test += [row_data]

    return np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

if __name__ == '__main__':
    conn = aws_context_db()
    indices = pull_all_lipo_ids(conn)

    seed(56)
    for i_shuffle in range(5):
        print(i_shuffle, datetime.now().time())
        shuffle(indices)
        k_folds = 5
        for k in range(k_folds):
            print(k, datetime.now().time())
            num_idx = len(indices)
            train_idx = [i for i in indices[0:(k*num_idx)//k_folds]]           \
                       +[i for i in indices[((k+1)*num_idx)//k_folds:num_idx]]
            test_idx = [i for i in indices[(k*num_idx)//k_folds:((k+1)*num_idx)//k_folds]]

            X_train, X_test, y_train, y_test = \
                test_train_data(conn, train_idx, test_idx)

            rf = RandomForestRegressor(n_estimators = 1000, max_depth=10, n_jobs = -1)
            rf.fit(X_train, y_train)
            print('Naive: ', rf.score(X_train, y_train))
            print(mean_squared_error(y_train, rf.predict(X_train)))

            print('Test:  ', rf.score(X_test,y_test))
            print(mean_squared_error(y_test, rf.predict(X_test)))
