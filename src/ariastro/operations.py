# The functions to perform mathematical operations
import numpy as np

'''
Mathematical operations
'''


def ari_operations(arr1, arr2, operation='sum'):
    if operation == 'sum':
        return arr1 + arr2
    elif operation == 'diff':
        return arr1 - arr2
    elif operation == 'prod':
        return arr1 * arr2
    elif operation == 'div':
        return arr1 / arr2


'''
Combine
'''


def combine_data(dataarr, var=None, method='mean'):
    # print('dataarr', dataarr)
    N = dataarr.shape[0]
    if method == 'mean':
        comb_data = np.nanmean(dataarr, axis=0)
    elif method == 'median':
        comb_data = np.nanmedian(dataarr, axis=0)

    # Propagating error.
    # Treating the error propagation
    # as mean for median also.
    if var is not None:
        comb_var = np.sum(var, axis=0) / N**2
        return comb_data, comb_var

    return comb_data


def combine_data_full(datadict, dataext=[1, 2, 3],
                      varext=[4, 5, 6],
                      method='mean'):
    dictkeys = list(datadict.keys())
    comb_dicts = datadict
    # print("comb data full", np.array(datadict["SCIFLUX"]).shape)
    flux_keys = [dictkeys[i] for i in dataext]
    var_keys = [dictkeys[i] for i in varext]

    # Avoiding the extensions that are not flux or variance.
    # Taking only the first element of that. i.e.,
    # The data from first fits file will
    # be copied to the final output.
    # For spectrum, wavelengths are interpolated to
    # same array. So, that also
    # copied in the same way.
    for cro, keys in enumerate(dictkeys):
        if keys not in flux_keys + var_keys:
            comb_dicts[keys] = comb_dicts[keys][0]
    # Doing for flux and variance.
    for index, extk in enumerate(flux_keys):
        fluxes = comb_dicts[flux_keys[index]]
        variances = comb_dicts[var_keys[index]]
        comb_flux, comb_var = combine_data(fluxes, variances)
        comb_dicts[flux_keys[index]] = fluxes
        comb_dicts[var_keys[index]] = variances
    # print(datadict[flux_keys[0]].shape)
    return comb_dicts

# End
