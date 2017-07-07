'''
A sample script to run an mcmc chain. We assume that all of the data has been
prepared in the "in_dir" folder. It outputs a file containing executable commands
used in the mock creations. This script is called by a bash script "test_mcmc.sh"
where passed parameters are specified.
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import mw_utilities_python as mwu
import sys, os
import numpy as np

data_dir='./out_data/'

def main():

    stats_fname='../out_data/normdiff_100chains.dat'
    if not os.path.isfile(stats_fname):
        sys.stderr.write('Error: {} does not exist.\n')

    pvalue_est = np.genfromtxt(stats_fname, unpack=True, usecols=5)
    # pvalue_true = np.genfromtxt('pvalue_truth_correct.dat')
    pvalue_true = pvalue_est/2

    pvalue_diff = pvalue_est - pvalue_true

    # plot results
    plt.clf()
    plt.figure(1)
    plt.plot(pvalue_est, pvalue_diff, 'bo')
    plt.xlabel(r'$P_{est}$')
    plt.ylabel(r'$P_{est} - P_{true}$')
    plt.savefig('pvalue_comparison.png')


if __name__ == '__main__':
    main()
