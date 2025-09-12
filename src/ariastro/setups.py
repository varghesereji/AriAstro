import argparse


def read_args():
    '''
    Read the argument while execution.
    '''

    parser = argparse.ArgumentParser(description="Input data to combine")
    parser.add_argument('operation', type=str,
                        choices=["operation", "combine"],
                        help="Required operation.")

    parser.add_argument('--fnames', required=True, nargs="+",
                        help="Input file names")
    parser.add_argument('--opfname', required=True,
                        help="Filename for output")
    parser.add_argument(
        '--instrument',
        type=str,
        help="If the data is from any specific inistrument (eg:NEID)"
    )

    subparsers = parser.add_subparsers(dest="mode", required=True,
                                       help="Choose mode")

   # --- operation subcommand ---
    op_parser = subparsers.add_parser("operation", help="Perform arithmetic operation")
    op_parser.add_argument("operator", choices=["+", "-", "*", "/"],
                           help="Arithmetic operator")

    # --- combine subcommand ---
    comb_parser = subparsers.add_parser("combine", help="Combine data")
    comb_parser.add_argument("method", choices=["mean", "median", "biweight"],
                             help="Combination method")
    return parser

# End
