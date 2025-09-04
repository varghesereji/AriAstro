#!/usr/bin/env python

from pathlib import Path
from astropy.io import fits
import numpy as np
import logging

from collections import defaultdict

from .logger import logger
from .interpolation import interpolation_spectra
from .setups import read_args
from .operations import combine_data


def setup_logging():
    logging.basicConfig(
        filename='ariastro_comb.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )


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


def get_data(hdu, fluxext, wlext, varext):
    '''
    Extracting data from hdu
    '''
    datadict = {'flux': np.array(hdu[fluxext].data).astype(np.float64),
                'wl': np.array(hdu[wlext].data).astype(np.float64)}
    if varext is not None:
        datadict['var'] = np.array(hdu[varext].data).astype(np.float64)
    return datadict


def combine_spectra(filesre="*.fits", directory=".",
                    opfilename="Comb_spectra.fits",
                    fluxext=(1, 2, 3),
                    varext=(4, 5, 6),
                    wlext=(7, 8, 9),
                    orders=(173, 52)):
    '''
    Function to combine spectra.
    Input
    -------
    filesre: Regular expression for the files.
    directory: data directory.
    fluxext: extension for flux array.

    '''
    # print(filesre)
    if isinstance(filesre, list):
        files_list = filesre
    elif isinstance(filesre, str):
        files_path = Path(directory)
        files_list = files_path.glob(filesre)
    else:
        print("Enter either files list or the regular expression")
        return

    data_dict = defaultdict(list)
    header_dict = {}
    flag = 0
    file_list = []
    for cro, specfile in enumerate(files_list):
        specfile = Path(specfile)
        logger.info("{} {}".format(cro, specfile))
        file_list.append(specfile.name)
        hdulist = fits.open(specfile)
        for i, hdu in enumerate(hdulist):
            extname = hdu.header.get('EXTNAME', f'HDU{i}')
            # print(i, extname)
            try:
                data = np.array(hdulist[i].data).astype(np.float64)
            except TypeError:
                data = np.array(hdulist[i].data)
            data_dict[extname].append(data)
            if flag == 0:
                header_dict[extname] = hdulist[i].header
        flag += 1

        hdulist.close()
    interp_data_dict = interpolation_spectra(data_dict, fluxext, wlext, varext)
    combined_dict = combine_data(interp_data_dict)
    # print(combined_dict)
    header_dict['HDU0']['HISTORY'] = "Combined {}".format(list(file_list))
    create_fits(combined_dict, header_dict,
                filename=Path(directory) / opfilename)
    # print(header_dict)
    del data_dict
    # print(np.array(flux).shape)


def main():
    parser = read_args()
    args = parser.parse_args()
    fnames = args.fnames
    logger.info("Starting the pipeline")
    # print(args.fnames)
    # print(fnames)
    # print(args.opfname)
    if args.operation == 'combine':
        combine_spectra(filesre=fnames,
                        opfilename=args.opfname)
    # if args.operation == 'combine':
    #     combine_spectra()
    #


if __name__ == '__main__':
    setup_logging()
    # path = '/home/varghese/Desktop/test_arastro'
    # filesre = "*T16*fits"
    # # filesre = list(Path(path).glob('*.fits'))
    # combine_spectra(filesre, path, opfilename="Comb_spectra.fits")
