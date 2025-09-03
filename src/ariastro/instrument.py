from astropy.io import fits
import numpy as np


def barycentric_corr_NEID(hdulist, wlext):
    headerext = 0
    headerkw = 'SSBZ'
    wlarray = np.array(hdulist[wlext].data).astype(np.float64)
    # print(wlarray.shape)
    wl_corr_arr = None
    for index, wlar in enumerate(wlarray):
        strnum = str(173 - index)
        while len(strnum) < 3:
            strnum = '0' + strnum
        # print(hdulist[headerext].header)
        zfact = hdulist[headerext].header[headerkw + strnum]
        wl_corr = wlar * (1+zfact)
        if wl_corr_arr is None:
            wl_corr_arr = wl_corr
        else:
            wl_corr_arr = np.vstack((wl_corr_arr, wl_corr))
    print("Corrected", wl_corr_arr.shape)
    

# End
