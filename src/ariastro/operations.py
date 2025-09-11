# The functions to perform mathematical operations
import numpy as np

'''
Mathematical operations
'''


def ari_operations(arr1, arr2, var_arr1=None, var_arr2=None, operation='sum'):
    """
    Perform element-wise arithmetic operations on two input arrays with
    optional variance propagation.

    Parameters
    ----------
    arr1 : numpy.ndarray
        First input array.
    arr2 : numpy.ndarray
        Second input array, must be broadcastable to the shape of `arr1`.
    var_arr1 : numpy.ndarray or None, optional
        Variance (uncertainty) array corresponding to `arr1`. Default is None.
    var_arr2 : numpy.ndarray or None, optional
        Variance (uncertainty) array corresponding to `arr2`. Default is None.
    operation : str, optional
        Arithmetic operation to apply (default is 'sum').
        Supported values:
        - 'sum'  : element-wise addition
        - 'diff' : element-wise subtraction (`arr1 - arr2`)
        - 'prod' : element-wise multiplication
        - 'div'  : element-wise division (`arr1 / arr2`)

    Returns
    -------
    numpy.ndarray or tuple of numpy.ndarray
        If `var_arr1` and `var_arr2` are not provided, returns the result of
        element-wise operation on `arr1` and `arr2`.
        If both variances are provided, returns the propagated variance array
        computed according to the operation:
        - For 'sum' and 'diff': variances are added.
        - For 'prod' and 'div': variance propagated as
    product.

    Raises
    ------
    ZeroDivisionError
        When division by zero occurs in 'div' operation.
    ValueError
        If `operation` is not one of the supported strings.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1.0, 2.0, 3.0])
    >>> b = np.array([4.0, 5.0, 6.0])
    >>> ari_operations(a, b, operation='sum')
    array([5., 7., 9.])
    >>> var_a = np.array([0.1, 0.1, 0.1])
    >>> var_b = np.array([0.2, 0.2, 0.2])
    >>> ari_operations(a, b, var_a, var_b, operation='sum')
    array([0.3, 0.3, 0.3])
    """
    if operation == 'sum':
        answer = arr1 + arr2
    elif operation == 'diff':
        answer = arr1 - arr2
    elif operation == 'prod':
        answer = arr1 * arr2
    elif operation == 'div':
        answer = arr1 / arr2
    else:
        raise ValueError(
            f"Unsupported operation '{operation}'. Supported: ",
            "'sum', 'diff', 'prod', 'div'.")

    if (var_arr1 is not None) & (var_arr2 is not None):
        if (operation == 'sum') or (operation == 'diff'):
            var_tot = var_arr1 + var_arr2
        elif (operation == 'prod') or (operation == 'div'):
            var_tot = answer**2 * ((var_arr1/arr1**2) + (var_arr2/arr2**2))
        return answer, var_tot

    return answer


'''
Combine
'''


def combine_data(dataarr, var=None, method='mean'):
    # print('dataarr', dataarr)
    dataarr = np.array(dataarr)
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
