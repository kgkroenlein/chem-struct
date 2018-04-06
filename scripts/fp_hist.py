import matplotlib.pyplot as plt
import pickle
import numpy as np
import psycopg2
import os

'''
Script for generating histograms off of fingerprint neighborhood distributions
'''
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

def gather_hist(conn = aws_context_db(), table='lipophilicity'):
    '''
    Gather the fingerprint nearest neighbors

    Inputs:
    conn: {psycopg2 connection} DB connection; defaults to aws_context_db()
    table: which data table to explore, with a default of lipophilicity

    Returns:
    Dictionary of dictionaries of how many nearset neighbors each compound in
    the lipophilicity table has, indexed by molregno
    '''
    results = dict()
    for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
        sql = '''
        SELECT  t1.molregno regno,
                COUNT(*)
        FROM    {} t1,
                {} t2,
                rdk.fps f1,
                rdk.fps f2,
                tanimoto_sml( f1.{}, f2.{} ) AS similarity
        WHERE   f1.{} % f2.{}
          AND   t1.molregno = f1.molregno
          AND   t2.molregno = f2.molregno
        GROUP BY t1.molregno;
        '''.format(table,table,fp,fp,fp,fp)

        cur = conn.cursor()
        cur.execute(sql)
        results[fp] = dict()
        for row in cur:
            results[fp][row[0]] = row[1]

    return results

def gather_others_hist(conn = aws_context_db(), table='lipophilicity'):
    '''
    Gather the labeled fingerprint nearest neighbors for a random sample of
    compounds not in the label set

    Inputs:
    conn: {psycopg2 connection} DB connection; defaults to aws_context_db()
    table: which data table to explore, with a default of lipophilicity

    Returns:
    Dictionary of dictionaries of how many nearset neighbors each compound in
    the lipophilicity table has, indexed by molregno
    '''
    results = dict()
    for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
        cur = conn.cursor()
        cur.execute('SELECT setseed(0.42);')
        for row in cur:
            pass # Clear the cursor

        sql = '''
        SELECT  t1.molregno regno,
                COUNT(*)
        FROM    (
                SELECT  molregno,
                FROM    compound_structures
                WHERE   molregno NOT IN (SELECT molregno FROM {})
                ORDER BY RANDOM()
                LIMIT 1000
                ) AS t1,
                {} t2,
                rdk.fps f1,
                rdk.fps f2,
                tanimoto_sml( f1.{}, f2.{} ) AS similarity
        WHERE   f1.{} % f2.{}
          AND   t1.molregno = f1.molregno
          AND   t2.molregno = f2.molregno
        GROUP BY t1.molregno;
        '''.format(table, table,fp,fp,fp,fp)

        cur.execute(sql)
        results[fp] = dict()
        for row in cur:
            results[fp][row[0]] = row[1]

    return results

def store_data(data, filename = 'hist_data.pkl'):
    '''
    Pickle the passed dictionary of dictionary of neighbor counts

    filename: {str} File name, default of 'hist_data.pkl'
    '''
    with open(filename, 'wb') as f:
        pickle.dump(data,f)

    return

def get_data(filename = 'hist_data.pkl'):
    '''
    Unpickle and return dictionary of dictionary of neighbor counts

    filename: {str} File name, default of 'hist_data.pkl'
    '''
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    return data

def plot_data(data):
    '''
    Generate histograms of dictionary of dictionary of neighbor counts
    '''
    cols = (1+len(data)) // 2
    plt.subplots(2,cols, figsize=[12,8])
    for i, fp_name in enumerate(data):
        ax = plt.subplot(2,3,i+1)
        counts = np.array([x for x in data[fp_name].values()])
        ax.hist(counts, bins=np.arange(1,counts.max()+1))
        ax.set_title(fp_name)
    plt.show()

if __name__ == '__main__':
    data = get_data()
    plot_data(data)
