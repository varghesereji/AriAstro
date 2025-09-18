Quickstart
==========

Run **AriAstro** using:

.. code-block:: bash

    ariastro <mode> <method> --fnames <FNAMES> [FNAMES ...] --output <OUTPUT> [--flux <FLUXEXT>] [--var <VAREXT>] [--wl <WLEXT>]

For help:

.. code-block:: bash

    ariastro --help


Combine Frames
==============

To combine multiple FITS files (e.g., file1.fits, file2.fits, file3.fits) with the **mean**, run:

.. code-block:: bash

    ariastro combine mean --fnames file1.fits file2.fits file3.fits --output <OUTPUT_NAME> --flux <FLUX_EXTENSIONS> --var <VARIANCE_EXTENSIONS>

Other options:

- Replace `mean` with `median` or `biweight`.
- Use regular expressions to select files:

.. code-block:: bash

    ariastro combine mean --fnames file*.fits --output <OUTPUT_NAME> --flux <FLUX_EXTENSIONS> --var <VARIANCE_EXTENSIONS>

For specific instruments (e.g., **NEID**):

.. code-block:: bash

    ariastro combine mean --fnames file*.fits --output <OUTPUT_NAME> --instrument NEID


Binary Operations
===========

For binary operations (`+`, `-`, `*`, `/`):

.. code-block:: bash

    ariastro operation <op> --fnames file1.fits file2.fits --output <OUTPUT_NAME> --flux <FLUX_EXTENSIONS> --var <VARIANCE_EXTENSIONS>

Example: subtract background (file1.fits - bkg1.fits):

.. code-block:: bash

    ariastro operation - --fnames file1.fits bkg1.fits --output <OUTPUT_NAME> --flux <FLUX_EXTENSIONS> --var <VARIANCE_EXTENSIONS>
