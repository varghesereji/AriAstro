import numpy as np
import pytest

from ariastro.operations import ari_operations
from ariastro.operations import combine_data
from ariastro.operations import combine_data_full


@pytest.mark.parametrize(
    "arr1, arr2, var_arr1, var_arr2, operation, expected, expected_var",
    [
        (np.array([1, 2]), np.array([3, 4]), None, None,
         'sum', np.array([4, 6]), None),
        (np.array([5, 7]), np.array([2, 3]), None, None,
         'diff', np.array([3, 4]), None),
        (np.array([2, 3]), np.array([4, 5]), None, None,
         'prod', np.array([8, 15]), None),
        (np.array([8, 9]), np.array([2, 3]), None, None,
         'div', np.array([4.0, 3.0]), None),
        (1, 1, None, None, 'sum', 2, None),
        (1, 1, 1, 1, 'sum', 2, 2)
    ]
)
def test_add(arr1, arr2,
             var_arr1, var_arr2,
             operation,
             expected, expected_var):
    if (var_arr1 is None) and (var_arr2 is None):
        result = ari_operations(arr1, arr2, var_arr1, var_arr2, operation)
        assert np.allclose(result, expected)
    else:
        result, variance = ari_operations(arr1, arr2,
                                          var_arr1, var_arr2,
                                          operation)
        assert np.allclose(result, expected)
        assert np.allclose(variance, expected_var)


@pytest.mark.parametrize(
    "dataarr, var, method, expected_data, expected_var",
    [
        # Mean without var
        (np.array([[1, 2], [3, 4]]), None, 'mean', np.array([2, 3]), None),

        # Median without var
        (np.array([[1, 2], [3, 4]]), None, 'median', np.array([2, 3]), None),

        # Mean with var
        (np.array([[1, 2], [3, 4]]), np.array([[0.1, 0.2], [0.1, 0.4]]),
         'mean', np.array([2, 3]), np.array([0.05, 0.15])),

        # Median with var
        (np.array([[1, 2], [3, 4]]), np.array([[0.1, 0.2], [0.1, 0.4]]),
         'median', np.array([2, 3]), np.array([0.05, 0.15])),
    ]
)
def test_combine_data(dataarr, var, method, expected_data, expected_var):
    if var is not None:
        comb_data, comb_var = combine_data(dataarr, var=var, method=method)
        assert np.allclose(comb_data, expected_data)
        assert np.allclose(comb_var, expected_var)
    else:
        comb_data = combine_data(dataarr, var=var, method=method)
        assert np.allclose(comb_data, expected_data)


def test_combine_data_full_basic():
    key0 = [None, None]
    scifluxes = np.arange(3*3*3).reshape(3, 3, 3)
    scivars = np.arange(3*3*3).reshape(3, 3, 3)
    wls = np.array([[500, 600],
                    [700, 800]])
    # mean_scifluxes = np.mean(scifluxes, axis=0)
    mean_flux, var_flux = combine_data(scifluxes, scivars, method='mean')
    datadict = {
        "KEY0": key0,
        "SCIFLUX": scifluxes,
        "VAR": scivars,
        "WAVELENGTH": wls
    }
    print(datadict["WAVELENGTH"])
    combined = combine_data_full(datadict, dataext=[1], varext=[2],
                                 method='mean')
    # Check that non-flux/var keys are replaced by first element
    print(datadict["WAVELENGTH"])
    assert np.array_equal(combined["SCIFLUX"], mean_flux)
    assert np.array_equal(combined["VAR"], var_flux)
    assert np.array_equal(combined["WAVELENGTH"], wls[0])
    assert combined["KEY0"] == key0[0]
    # Check combined flux and variance (example expectations)
    # Depend on fixed combine_data behavior
    # For example:
    # expected_flux = np.array([2.0, 3.0])  # mean of [1,3] and [2,4]
    # expected_var = np.array([0.01, 0.025])  # example propagated variance
