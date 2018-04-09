import matplotlib.pyplot as plt
import pickle
import numpy as np
from collections import defaultdict

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
    fps  = restore_data('np_fps.pkl')

    skipped = 0
    res = defaultdict(dict)
    ss = defaultdict(lambda:0)
    tot = defaultdict(lambda:0)
    i = 0
    for id in fps:
        i += 1
        if (i % 100) == 0:
            print(i)
        norm = defaultdict(lambda:0)
        summ = defaultdict(lambda:0)
        for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
            for n_id in nmap[fp][id]:
                if nmap[fp][id][n_id] != 1: #and nmap[fp][id][n_id] > .6:
                    weight = np.exp(25.0*nmap[fp][id][n_id])
                    norm[fp] += weight
                    summ[fp] += fps[n_id]['value']*weight
            if norm[fp] == 0:
                continue
            res[fp][id] = fps[id]['value'] - summ[fp]/norm[fp]
            tot[fp] += fps[id]['value']
            ss[fp] += fps[id]['value']**2
    for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
        print (fp, 1 - sum([i**2 for i in res[fp].values()])/(ss[fp] - tot[fp]**2/len(res[fp])))

    med_res = dict()
    med_ss = 0
    med_tot = 0
    for id in fps.keys():
        med_ss += fps[id]['value']**2
        med_tot += fps[id]['value']
        this = []
        for fp in ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs'):
            if id in res[fp]:
                this += [res[fp][id]]
        n = len(this)
        med_res[id] = 0.5*(sorted(this)[n//2] + sorted(this)[(n-1)//2])
    print ('median', 1 - sum([i**2 for i in med_res.values()])/(med_ss - med_tot**2/len(res[fp])))
