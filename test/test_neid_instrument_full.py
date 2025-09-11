import numpy as np
import pytest
from astropy.io import fits
from ariastro import Handle_NEID


@pytest.fixture
def dummu_fits(tmp_path):
    """
    Create a dummy fits file with multiple extensions
    to simulate NEID data
    """
    sci = fits.ImageHDU(data=np.ones((10)))
    var = fits.ImageHDU(data=np.full((10,), 0.1))
    wl = fits.ImageHDU(data=np.linspace(500, 600, 10))

    blaze = fits.ImageHDU(data=np.linspace(0.5, 1.5, 10))
    hdul = fits.HDUList([fits.PrimaryHDU(), sci, var, wl, blaze])
    file_path = tmp_path / "dummy.fits"
    hdul.writeto(file_path)
    return str(file_path)
