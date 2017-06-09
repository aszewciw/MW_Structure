import sys, os
import numpy as np
import pandas as pd
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_chi2(data, model, invcov):

    chi2 = 0.0

    for i in range(len(data)):

        for j in range(len(data)):

            Di = data[i]
            Dj = data[j]
            Mi = model[i]
            Mj = model[j]
            Cij = invcov[i,j]

            chi2 += (Di-Mi)*(Dj-Mj)*Cij

    return(chi2)


def main():

    data_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/sample_56/'
    mm_dir = '../pair_count_nonuni/data/'
    err_rid_dir = '../prep_ridiculous_mocks/errors_data/'
    err_true_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_fid_errors_DATAPARAMS/errors_data/'
    err_fid_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_fid_errors/errors_data/'
    ID_file = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_fidcov_nonuni/data/pointing_ID.dat'

    ID_list = np.genfromtxt(ID_file, skip_header=1)


    for ID in ID_list:
        ID = str(ID)
        sys.stderr.write('On pointing {}'.format(ID))

        dd_file = data_dir + 'dd_' + ID + '.dat'
        dd = np.genfromtxt(dd_file, unpack=True, usecols=[4])

        mm_file = mm_dir + 'mm_ridiculous_' + ID + '.dat'
        mm_rid = np.genfromtxt(mm_file, unpack=True, usecols=[4])
        mm_file = mm_dir + 'mm_truth_' + ID + '.dat'
        mm_true = np.genfromtxt(mm_file, unpack=True, usecols=[4])

        # Fiducial corr matrix
        corr_file = err_fid_dir + 'correlation_' + ID + '.dat'
        fid_corr = pd.read_csv(corr_file, sep='\s+', header=None)

        # True corr matrix
        corr_file = err_true_dir + 'correlation_' + ID + '.dat'
        true_corr = pd.read_csv(corr_file, sep='\s+', header=None)

        # Ridiculous corr matrix
        corr_file = err_rid_dir + 'correlation_' + ID + '.dat'
        rid_corr = pd.read_csv(corr_file, sep='\s+', header=None)

        # Fiducial mean and std
        stats_file = err_fid_dir + 'mean_std_' + ID + '.dat'
        fid_mean, fid_std = np.genfromtxt(stats_file, unpack=True)

        # Fiducial mean and std
        stats_file = err_true_dir + 'mean_std_' + ID + '.dat'
        true_mean, true_std = np.genfromtxt(stats_file, unpack=True)

        # Fiducial mean and std
        stats_file = err_rid_dir + 'mean_std_' + ID + '.dat'
        rid_mean, rid_std = np.genfromtxt(stats_file, unpack=True)

if __name__ == '__main__':
    main()