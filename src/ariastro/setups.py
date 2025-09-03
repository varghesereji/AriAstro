import argparse

def read_args():
    '''
    Read the argument while execution.
    '''

    parser = argparse.ArgumentParser(description="Input data to combine")
    parser.add_argument('fnames', type=str, help="Input file names")
    return parser
