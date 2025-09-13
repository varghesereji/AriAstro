from astropy.io import fits
from .operations import ari_operations


def operate_process(ip1, ip2,
                    opfilename,
                    operation='+',
                    fluxext=[0],
                    varext=None):
    """
    Perform arithmetic operations on FITS file extensions and write results.

    This function takes one FITS file (``ip1``) and either another FITS file
    or a constant value (``ip2``), performs the specified operation on the
    selected extensions, and writes the result to a new FITS file.

    Parameters
    ----------
    ip1 : str
        Path to the first FITS file.
    ip2 : str or float
        Path to the second FITS file, or a constant value to apply the
        operation.
        - If a filename, the same extensions as in ``fluxext`` will be read.
        - If a float, the value is broadcasted to the data in ``ip1``.
    opfilename : str
        Output FITS filename where the result will be written.
    operation : {'+', '-', '*', '/', ...}, optional
        Arithmetic operation to perform. Default is ``'+'``.
        The valid set depends on what ``ari_operations`` supports.
    fluxext : list of int, optional
        List of extension numbers containing flux data in the input files.
        Each extension in this list will be processed. Default is ``[0]``
        (primary HDU).
    varext : list of int or None, optional
        List of extension numbers containing variance data corresponding to
        each entry in ``fluxext``. If ``None`` (default), variance propagation
        is skipped.

    Notes
    -----
    - For each extension in ``fluxext``:
      
      1. Data are read from ``ip1`` and ``ip2``.
      2. The operation is applied using ``ari_operations``.
      3. Results are stored in the output HDUList.
      4. If ``varext`` is provided, the corresponding variance extensions are
         also operated on and appended to the output.

    - If an extension index is ``0``, the result is stored in the
      ``PrimaryHDU``. Otherwise, results are stored as ``ImageHDU``
      extensions.

    - A ``HISTORY`` entry is added to the output headers to track
      the operation.

    Examples
    --------
    Add fluxes in the primary HDU of two FITS files::

        operate_process("file1.fits", "file2.fits",
                        "sum.fits", operation='+', fluxext=[0])

    Subtract a constant value from a flux extension::

        operate_process("file1.fits", 10.0,
                        "output.fits", operation='-', fluxext=[1])

    Perform multiplication with variance propagation::

        operate_process("file1.fits", "file2.fits",
                        "multiplied.fits", operation='*',
                        fluxext=[1, 2], varext=[3, 4])
    """

    primary_hdu = fits.PrimaryHDU()
    hdul = fits.HDUList([primary_hdu])
    for index, ext in enumerate(fluxext):
        ext = int(ext)
        header = fits.getheader(ip1, ext=ext)
        hdul1 = fits.open(ip1)
        data1 = hdul1[ext].data
        header['HISTORY'] = '{} {} {}'.format(ip1, operation, ip2)
        if varext is None:
            var1 = None
        else:
            var1 = hdul1[int(varext[index])].data
        hdul1.close()

        if isinstance(ip2, float):
            data2 = ip2
            var2 = 0
        else:
            hdul2 = fits.open(ip2)
            data2 = hdul2[ext].data
            if varext is None:
                var2 = None
            else:
                var2 = hdul2[int(varext[index])].data
            hdul2.close()
        result, var = ari_operations(data1, data2,
                                     var1, var2,
                                     operation=operation)
        if int(ext) == 0:
            hdul[0] = fits.PrimaryHDU(result, header=header)
        else:
            imagehdu = fits.ImageHDU(result, header=header)
            hdul.append(imagehdu)
        if varext is not None:
            hdul.append(
                fits.ImageHDU(var,
                              header=fits.getheader(
                                  ip1, ext=int(varext[index])
                              )
                              )
            )
    hdul.writeto(opfilename, overwrite=True)


# End
