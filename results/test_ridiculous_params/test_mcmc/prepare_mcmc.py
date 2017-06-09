'''
A sample script to run an mcmc chain. We assume that all of the data has been
prepared in the "in_dir" folder. It outputs a file containing executable commands
used in the mock creations. This script is called by a bash script "test_mcmc.sh"
where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    data_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/sample_56/'
    dd_dir = './data/'

    if not os.path.isdir(dd_dir):
        cmd='mkdir ' + dd_dir
        os.system(cmd)


    for i in range(164):

        fname = data_dir + 'dd_' + str(i) + '.dat'

        if not os.path.isfile(fname):
            continue

        dd = np.genfromtxt(fname, unpack=True, usecols=[4])

        dd_fname = dd_dir + 'DD_' + str(i) + '.dat'
        with open(dd_fname, 'w') as f:
            for d in dd:
                f.write('{0:.6e}\n'.format(d))



if __name__ == '__main__':
    main()
