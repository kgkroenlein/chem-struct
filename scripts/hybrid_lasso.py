import matplotlib.pyplot as plt
import pickle
import numpy as np
from collections import defaultdict
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoLarsIC

def restore_data(filename = 'hist_data.pkl'):
    '''
    Unpickle and return dictionary of dictionary of neighbor counts

    filename: {str} File name, default of 'hist_data.pkl'
    '''
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    return data

if __name__ == '__main__':
    nmap = restore_data('neighbors.pkl')
    fps_in  = restore_data('np_fps.pkl')

    fps = dict()
    for id in fps_in:
        tmp  = fps_in[id]['mfp2']
        for fp in ('ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
            tmp = np.append(tmp, fps_in[id][fp])
        fps[id] = tmp

    res = dict()
    ss = 0
    tot = 0
    i = 0
    for id in fps:
        i += 1
        if (i % 100) == 0:
            print(i)

        # Collect ids
        ids = {id}
        for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
            for n_id in nmap[fp][id]:
                if n_id not in ids:
                    ids.add(n_id)
        ids.remove(id) # No cheating!

        X = []
        y = []
        for n_id in ids:
            X += [fps[n_id]]
            y += [fps_in[n_id]['value']]

        pred = Lasso().fit(X,y).predict(fps[id].reshape(1, -1))
        res[id] = fps_in[id]['value'] - pred
        tot += fps_in[id]['value']
        ss += fps_in[id]['value']**2

    print (fp, 1 - sum([i**2 for i in res.values()])/(ss - tot**2/len(res)))
