#!/usr/bin/env python

from pathlib import Path
from astropy.io import fits
import numpy as np
import logging

from collections import defaultdict

from .logger import logger
from .spectral_utils import interpolation_spectra
from .setups import read_args
from .operations import combine_data
from .utils import create_fits
from .instrument import instrument_dict


def setup_logging():
    logging.basicConfig(
        filename='ariastro_comb.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )


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
    headerdict_main = None
    file_list = []
    for cro, specfile in enumerate(files_list):
        specfile = Path(specfile)
        # print(specfile)
        logger.info("{} {}".format(cro, specfile))
        file_list.append(specfile.name)
        instrument = instrument_dict["NEID"]()

        datadict, headerdict = instrument.process_data(fname=specfile,
                                                       contnorm=True)
        if headerdict_main is None:
            headerdict_main = headerdict

        for hduname, data in datadict.items():
            # print(hduname)
            data_dict[hduname].append(data)

    interp_data_dict = interpolation_spectra(data_dict, fluxext, wlext, varext)
    combined_dict = combine_data(interp_data_dict)
    # # print(combined_dict)
    dict_keys = list(headerdict_main.keys())

    headerdict_main[dict_keys[0]]['HISTORY'] = "Combined {}".format(
        list(file_list))

    logger.info("Combining spectra")
    create_fits(combined_dict, headerdict_main,
                filename=Path(directory) / opfilename)
    logger.info("Combined spectra")
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
