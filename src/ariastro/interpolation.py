import numpy as np
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)

from scipy.interpolate import CubicSpline



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
        print(header_wl, header_fl, header_va)

        flux_data = np.array(fulldata[header_fl])
        wl_data = np.array(fulldata[header_wl])
        var_data = np.array(fulldata[header_va])

        ref_wl = wl_data[0]
        # print(np.size(wl_data))
        for epoin, epodata in enumerate(wl_data):
            # Goint through each epoch
            print("Epoch", epoin)
            logger.info("Epoch {}".format(epoin))
            epoch_flux = flux_data[epoin]
            epoch_wl = wl_data[epoin]
            epoch_var = var_data[epoin]
            
            for order, wl_order in enumerate(epoch_wl):
                # Goint through each order of the epoch
                # print(order, '==========================')
                logger.info("order {}".format(order))
                fl_order = epoch_flux[order]
                var_order = epoch_var[order]
                # plt.figure()
                # plt.plot(wl_order, fl_order, 'o-')
                # plt.show()
                data_nanmask = np.isnan(fl_order) | np.isnan(var_order) \
                    | np.isinf(fl_order) | np.isinf(var_order)
                wl_zeros = wl_order < 3000
                data_mask = data_nanmask | wl_zeros
                print(order, np.where(data_nanmask))
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
                epoch_wl[order] = ref_wl[order][order]
            flux_data[epoin] = epoch_flux
            wl_data[epoin] = epoch_wl
            var_data[epoin] = epoch_var

        fulldata[header_fl] = flux_data
        fulldata[header_wl] = wl_data
        fulldata[header_va] = var_data
    return fulldata        
                

# End
