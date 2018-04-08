from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
from rdkit import DataStructs


def aws_context_db():
    '''
    Connect to the standard deployment database
    '''
    conn = psycopg2.connect(database='chemstruct',
                            user='postgres',
                            host=os.environ['DB_PORT_5432_TCP_ADDR'],
                            port=os.environ['DB_PORT_5432_TCP_PORT'],
                            )
    return conn

def pull_data(fp, conn = None):
    import psycopg2
    import os
    '''
    Pull all fingerprints and the associated label from the database for
    lipophilicity table

    Input: fp {str}  Which fingerprint to pull:
            'mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'
    '''

    if not conn:
        conn = aws_context_db()

    sql = '''
    SELECT  rdk.fps.{} AS fp,
            lipophilicity.value AS val
    FROM    lipophilicity,
            rdk.fps
    WHERE   lipophilicity.molregno = fps.molregno
    ORDER BY    lipophilicity.molregno -- So splits aren't volitile
    '''.format(fp)

    cur = conn.cursor()
    cur.execute(sql)
    X = []
    y = []

    for row in cur:
        X += [fp2bits(row[0])]
        y += [row[1]]

    return np.array(X), np.array(y)

def fp2bits(fp):
    ebv = DataStructs.cDataStructs.CreateFromBitString(fp)
    stash = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(ebv, stash)
    return stash

def restore_data(fp, filename='fps.pkl'):
    import pickle
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    ids = [i for i in data] # Guarentee traversal order
    X = [fp2bits(data[id][fp]) for id in ids]
    y = [data[id]['value'] for id in ids]

    return np.array(X), np.array(y)

def train_rf(X, y):
    rf = RandomForestRegressor()
    rf.fit(X,y)
    return rf

if __name__ == '__main__':
    for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
        # X, y = pull_data(fp)
        X, y = restore_data(fp)
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=0.2, random_state=42)
        model = train_rf(X_train, y_train)
        print("{}:\t{:.4f}".format(fp,model.score(X_test, y_test)))
