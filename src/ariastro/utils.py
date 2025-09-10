from astropy.io import fits
import numpy as np


def extract_data_header(hdu, ext=0):
    """
    Function to open the fits file and
    extract the data and header.
    """
    data = hdu[ext].data
    header = hdu[ext].header
    extname = hdu[ext].header.get("EXTNAME")

    return data, header, extname


def extract_allexts(fname):
    hdu = fits.open(fname)
    datadict = {}
    headerdict = {}
    for ext in range(len(hdu)):
        data, header, extname = extract_data_header(hdu, ext=ext)
        datadict[extname] = data
        headerdict[extname] = header
    return datadict, headerdict


def create_fits(datadict, header_dict, filename="Avg_neid_data.fits"):
    '''
    The function to create the fits file.
    datadict: Dictionary of data. Dict keys will
    be the name of each extension.
    header dict: Header dictionary.
    filename: Name of the file with path.
    '''
    header_names = list(datadict.keys())
    hdus = []

    # --- Primary HDU ---
    primary_data = np.atleast_1d(datadict[header_names[0]])
    if primary_data.ndim == 1:
        primary_data = primary_data.reshape(1, -1)  # ensure 2D
    primary_header = fits.Header(header_dict[header_names[0]])
    primary_hdu = fits.PrimaryHDU(primary_data, header=primary_header)
    hdus.append(primary_hdu)

    # --- Extensions ---
    for exts in header_names[1:]:
        data = np.atleast_1d(datadict[exts])
        try:
            if data.ndim == 1:
                data = data.reshape(1, -1)  # ensure 2D
            ext_header = fits.Header(header_dict[exts])
            hdu = fits.ImageHDU(data, header=ext_header, name=exts)
        except KeyError:
            data = np.array([np.nan, np.nan])
            ext_header = fits.Header(header_dict[exts])
            hdu = fits.ImageHDU(data, header=ext_header, name=exts)
        hdus.append(hdu)

    # --- Write FITS ---
    hdul = fits.HDUList(hdus)
    hdul.writeto(filename, overwrite=True)



# End
