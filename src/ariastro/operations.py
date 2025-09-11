# The functions to perform mathematical operations
import numpy as np



def ari_operations(arr1, arr2, operation='sum'):
    if operation == 'sum':
        return arr1 + arr2
    elif operation == 'diff':
        return arr1 - arr2
    elif operation == 'prod':
        return arr1 * arr2
    elif operation == 'div':
        return arr1 / arr2


def combine_data(datadict, method='mean', skipexts=[0, 11, 13]):
    dictkeys = list(datadict.keys())
    comb_dicts = {}
    # print(dictkeys)
    for n, keys in enumerate(dictkeys):
        print(n, keys, skipexts)
        data = datadict[keys]
        if n in skipexts:
            comb_data = data[0]
        else:
            if method == 'mean':
                print(data)
                comb_data = np.nanmean(data, axis=0)
            elif method == 'median':
                comb_data = np.nanmedian(data, axis=0)
        comb_dicts[keys] = comb_data
    return comb_dicts

# End
