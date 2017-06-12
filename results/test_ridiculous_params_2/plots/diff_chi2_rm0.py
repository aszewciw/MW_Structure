import sys, os
import numpy as np
import pandas as pd
from scipy import linalg
from scipy.stats import chisqprob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_chi2(data, model, invcorr, sigma):

    chi2 = 0.0

    for i in range(len(data)):

        for j in range(len(data)):

            Di = data[i]
            Dj = data[j]
            Mi = model[i]
            Mj = model[j]
            Rij = invcorr[i,j]
            sigmai = sigma[i]
            sigmaj = sigma[j]
            if(sigmai==0.0):
                continue
            if(sigmaj==0.0):
                continue

            chi2 += (Di-Mi)*(Dj-Mj)*Rij/sigmai/sigmaj

    return(chi2)


def main():

    data_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/sample_56/'
    mm_dir = '../pair_count_nonuni/data/'
    err_rid_dir = '../prep_ridiculous_mocks/errors_data/'
    err_true_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_fid_errors_DATAPARAMS/errors_data/'
    err_fid_dir = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_fid_errors/errors_data/'
    ID_file = '/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_fidcov_nonuni/data/pointing_ID.dat'

    ID_list = np.genfromtxt(ID_file, skip_header=1, dtype=int)


    chi2_true = np.zeros(4)
    chi2_rid = np.zeros(4)

    for ID in ID_list:
        ID = str(ID)
        sys.stderr.write('On pointing {}\n'.format(ID))

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




        # Not excluding any bins for now


        fid_inv = linalg.inv(fid_corr.values)
        true_inv = linalg.inv(true_corr.values)
        rid_inv = linalg.inv(rid_corr.values)

        chi2_true[0] += compute_chi2(dd, mm_true, fid_inv, fid_std)
        chi2_true[1] += compute_chi2(dd, true_mean, fid_inv, fid_std)
        chi2_true[2] += compute_chi2(dd, mm_true, true_inv, true_std)
        chi2_true[3] += compute_chi2(dd, true_mean, true_inv, true_std)

        chi2_rid[0] += compute_chi2(dd, mm_rid, fid_inv, fid_std)
        chi2_rid[1] += compute_chi2(dd, rid_mean, fid_inv, fid_std)
        chi2_rid[2] += compute_chi2(dd, mm_rid, rid_inv, rid_std)
        chi2_rid[3] += compute_chi2(dd, rid_mean, rid_inv, rid_std)


    # print(chi2_rid)
    # print(chi2_true)
    Nbins = 12
    Nlos = 152
    dof = Nlos * Nbins

    pvalue_true = np.zeros(len(chi2_true))
    pvalue_rid = np.zeros(len(chi2_rid))
    for i in range(len(chi2_true)):
        pvalue_true[i] = chisqprob(chi2_true[i], dof)
        pvalue_rid[i] = chisqprob(chi2_rid[i], dof)

    plt.figure(1)
    x = np.arange(4) + 1

    plt.plot(x, pvalue_true, 'r', label='correct model')
    plt.plot(x, pvalue_rid, 'b', label='incorrect model')
    plt.ylabel(r'$\chi^2$')
    plt.legend(loc='upper left')
    plt.savefig('pvalue_comp.png')


if __name__ == '__main__':
    main()