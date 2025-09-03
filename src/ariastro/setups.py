import argparse


def read_args():
    '''
    Read the argument while execution.
    '''

    parser = argparse.ArgumentParser(description="Input data to combine")
    parser.add_argument('operation', type=str,
                        help="Required operation (operation, combine).")
    parser.add_argument('--fnames', required=True, nargs="+",
                        help="Input file names")
    parser.add_argument('--opfname', required=True,
                        help="Filename for output")
    return parser

# End
