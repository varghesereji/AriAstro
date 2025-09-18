Quickstart
===========

Run AriAstro via the following command.

.. code-block:: bash

		ariastro <mode> <method> --fnames FNAMES [FNAMES ...] --output [OUTPUT] [--flux FLUXEXT] [--var VAREXT] [--wl WLEXT]


To get help, enter

.. code-block:: bash
		
		ariastro --help


To combine file1.fits, file2.fits, file3.fits ..., with mean, enter

.. code-block:: bash
		
		ariastro combine mean --fnames file1.fits file2.fits file3.fits --output [OUTPUT_NAME] --flux [FLUX EXTENSIONS] --var [VARIANCE EXTENSIONS]

You can also use regular expression to list the files.

.. code-block:: bash
		
		ariastro combine mean --fnames file*.fits --output [OUTPUT_NAME] --flux [FLUX EXTENSIONS] --var [VARIANCE EXTENSIONS]



