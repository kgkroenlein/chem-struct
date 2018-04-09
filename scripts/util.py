import pickle
import psycopg2
import os

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

def store_data(data, filename = 'data.pkl'):
    '''
    Pickle the passed dictionary of dictionary of neighbor counts

    filename: {str} File name, default of 'hist_data.pkl'
    '''
    with open(filename, 'wb') as f:
        pickle.dump(data,f)

    return

def load_data(filename = 'data.pkl'):
    '''
    Unpickle and return dictionary of dictionary of neighbor counts

    filename: {str} File name, default of 'hist_data.pkl'
    '''
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    return data
