from sklearn.ensemble import RandomForestRegressor
from util import load_data
from random import sample
import numpy as np

if __name__ == '__main__':
    nmap = load_data('nmap.pkl')
    fp_data = load_data('np_fps.pkl')
    idx = {i for i in nmap['mfp2'].keys()}
    test_idx = sample(idx, len(idx)//5)

    fp_names = ('mfp2', 'ffp2', 'torsionbv', 'atompair', 'rdkitbv', 'maccs')
    X = []
    y = []
    for i in idx:
        if i in test_idx:
            continue
        y += [fp_data[i]['value']]
        X += [[]]
        for fp_name in fp_names:
            X[-1] += list(fp_data[i][fp_name])
            count = 0
            for neighbor in sorted(nmap[fp_name][i], key=nmap[fp_name][i].get, reverse=True):
                if neighbor in test_idx:
                    continue
                X[-1] += [nmap[fp_name][i][neighbor], fp_data[neighbor]['value']]
                count += 1
                if count == 5:
                    break

    rf = RandomForestRegressor(n_estimators = 1000, max_depth=10)
    rf.fit(np.array(X),np.array(y))
    print('Naive: ', rf.score(np.array(X),np.array(y)))

    X_test = []
    y_test = []
    for i in test_idx:
        y_test += [fp_data[i]['value']]
        X_test += [[]]
        for fp_name in fp_names:
            X_test[-1] += list(fp_data[i][fp_name])
            count = 0
            for neighbor in sorted(nmap[fp_name][i], key=nmap[fp_name][i].get, reverse=True):
                if neighbor in test_idx:
                    continue
                X_test[-1] += [nmap[fp_name][i][neighbor], fp_data[neighbor]['value']]
                count += 1
                if count == 5:
                    break
    print('Test:  ', rf.score(np.array(X_test),np.array(y_test)))
