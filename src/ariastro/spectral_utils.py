import numpy as np
import astropy.units as u
from scipy.interpolate import CubicSpline
from .logger import logger
try:
    from specutils.spectra import Spectrum
except ImportError:
    from specutils.spectra import Spectrum1D as Spectrum

from specutils.fitting import fit_generic_continuum


def interpolate_data(data, wl_new, wl_corr):
    '''
    data: The data to interpolate (eg flux)
    wl_new: x data to interpolate.
    wl_corr: x_new in interpolate function.
    '''

    cbs = CubicSpline(wl_new, data)
    corr_data = cbs(wl_corr)
    return corr_data


def interpolation_spectra(fulldata, fluxext, wlext, varext):
    '''
    fulldata: dictionary.
    '''
    keys = list(fulldata.keys())
    for index, wext in enumerate(wlext):
        # Goint though sci, cal and sky
        fext = fluxext[index]
        vext = varext[index]
        header_wl = keys[wext]
        header_fl = keys[fext]
        header_va = keys[vext]
        # print(header_wl, header_fl, header_va)

        flux_data = np.array(fulldata[header_fl])
        wl_data = np.array(fulldata[header_wl])
        var_data = np.array(fulldata[header_va])
        logger.info("Extensions: {} {} {}".format(
            wext, fext, vext))
        logger.info("Exten names: {} {} {}".format(
            header_wl, header_fl, header_va))

        ref_wl = wl_data[0]
        # print(np.size(wl_data))
        for epoin, epodata in enumerate(wl_data):
            # Goint through each epoch
            # print("Epoch", epoin)
            # logger.info("Epoch {}".format(epoin))
            epoch_flux = flux_data[epoin]
            epoch_wl = wl_data[epoin]
            epoch_var = var_data[epoin]

            for order, wl_order in enumerate(epoch_wl):
                # Goint through each order of the epoch
                # print(order, '==========================')
                # logger.info("order {}".format(order))
                fl_order = epoch_flux[order]
                var_order = epoch_var[order]
                # plt.figure()
                # plt.plot(wl_order, fl_order, 'o-')
                # plt.show()
                data_nanmask = np.isnan(fl_order) | np.isnan(var_order) \
                    | np.isinf(fl_order) | np.isinf(var_order)
                wl_zeros = wl_order < 3000
                data_mask = data_nanmask | wl_zeros
                if np.sum(data_mask) == np.size(fl_order):
                    interp_flux = fl_order
                    interp_var = var_order
                    continue
                else:
                    interp_flux = interpolate_data(fl_order[~data_mask],
                                                   wl_order[~data_mask],
                                                   ref_wl[order][~data_mask])
                    interp_var = interpolate_data(var_order[~data_mask],
                                                  wl_order[~data_mask],
                                                  ref_wl[order][~data_mask])

                    fl_order[~data_mask] = interp_flux
                    var_order[~data_mask] = interp_var

                epoch_flux[order] = fl_order
                epoch_var[order] = var_order
                # print("Ref wl", ref_wl[order
                epoch_wl[order] = ref_wl[order]
            flux_data[epoin] = epoch_flux
            wl_data[epoin] = epoch_wl
            var_data[epoin] = epoch_var

        fulldata[header_fl] = flux_data
        fulldata[header_wl] = wl_data
        fulldata[header_va] = var_data
    return fulldata


def continuum_normalize(datadict, flux_exts=[1],
                        var_exts=[4], wl_exts=[7]):
    """
    Perform continuum normalization on flux and variance arrays in
    a FITS-like data dictionary.

    This function iterates through selected extensions of the input `datadict`,
    fits a generic continuum to each spectrum, and then divides the flux and
    variance by the fitted continuum to flatten the spectra. This is useful for
    preparing echelle or multi-order spectra for further analysis.

    Parameters
    ----------
    datadict : dict
        Dictionary containing spectral data arrays keyed by FITS extension
    names
        (e.g., from `extract_allexts`). Must include flux, variance, and
        wavelength arrays.
    flux_exts : list of int, optional
        Indices (positions in `datadict.keys()`) of extensions containing flux
        arrays. Default is [1].
    var_exts : list of int, optional
        Indices of extensions containing variance arrays. Default is [4].
    wl_exts : list of int, optional
        Indices of extensions containing wavelength arrays. Default is [7].

    Returns
    -------
    datadict : dict
        Updated dictionary with continuum-normalized flux and variance arrays.
        The continuum-normalized values overwrite the original flux and
        variance arrays in the specified extensions.

    Notes
    -----
    - Spectra with only NaN or Inf values are skipped.
    - Continuum fitting is performed using `fit_generic_continuum` from
      `specutils`, with a median filter window of 15 pixels.
    - Variance is rescaled consistently with the normalized flux, i.e.,
      ``corr_var = var / continuum**2``.
    - Units:
        * Flux is assumed to be in photons (``u.ph``).
        * Wavelength is assumed to be in Angstroms (``u.AA``).

    Examples
    --------
    >>> from ariastro.utils import continuum_normalize
    >>> norm_datadict = continuum_normalize(datadict, flux_exts=[1,2,3],
    ...                                     var_exts=[4,5,6],
    ...                                     wl_exts=[7,8,9])
    >>> norm_flux = norm_datadict['SCI_FLUX_EXT1']
    """
    dict_keys = list(datadict.keys())

    for n, ext in enumerate(flux_exts):
        # n = 0
        flux_key = dict_keys[flux_exts[n]]
        var_key = dict_keys[var_exts[n]]
        wl_key = dict_keys[wl_exts[n]]

        flux_array = datadict[flux_key]
        var_array = datadict[var_key]
        wl_array = datadict[wl_key]

        for index in range(np.shape(flux_array)[0]):

            flux = flux_array[index]
            var = var_array[index]
            wl = wl_array[index]

            nanmask = np.isnan(flux) | np.isinf(flux)
            if np.sum(nanmask) == np.shape(flux)[0]:
                continue
            flux = flux[~nanmask]
            var = var[~nanmask]
            wl = wl[~nanmask]

            spectrum = Spectrum(flux=flux*u.ph, spectral_axis=wl*u.AA)
            g1_fit = fit_generic_continuum(spectrum, median_window=15)
            y_continuum_fitted = g1_fit(wl*u.AA)
            corr_flux = flux / y_continuum_fitted
            corr_var = var / y_continuum_fitted ** 2
            flux_array[index, ~nanmask] = corr_flux
            var_array[index, ~nanmask] = corr_var

        datadict[flux_key] = flux_array

    return datadict

# End
