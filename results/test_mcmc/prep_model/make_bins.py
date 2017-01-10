'''
Make a set of distance bins. Here we use defaults settings.
'''
import mw_utilities_python as mwu
import numpy as np
import sys, os

def main():

    # get out_dir
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    out_dir = args_array[1]

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    # Make default radial bins
    mwu.corr_prep.set_rbins(filepath=out_dir)

if __name__ == '__main__':
    main()