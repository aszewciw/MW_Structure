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

def make_bins(x, bwidth):

    bin_min=int(min(x))
    bin_max=int(max(x))+1

    bins=np.arange(bin_min,bin_max,bwidth)

    return bins


def main():

    Nfiles=100
    data_dir='./out_data/'

    # Make a dictionary to store statistics calculated for each chain
    pd_keys=['r0_thin', 'z0_thin', 'r0_thick', 'z0_thick', 'ratio']
    STATS={}
    for i in pd_keys:
        STATS[i]={}
        # Distribution median and standard deviation
        STATS[i]['median']=np.zeros(Nfiles)
        STATS[i]['std']=np.zeros(Nfiles)
        # (median-true)/std
        STATS[i]['normdiff']=np.zeros(Nfiles)

    STATS['r0_thin']['true']=2.027
    STATS['z0_thin']['true']=0.234
    STATS['r0_thick']['true']=2.397
    STATS['z0_thick']['true']=0.675
    STATS['ratio']['true']=0.053


    # Load results of each chain and compute stats
    for i in range(Nfiles):
        if(i%10==0):
            sys.stderr.write('On result #{} of {}\n'.format(i,Nfiles))
        fname = data_dir + 'results_' + str(i) + '.dat'
        if not os.path.isfile(fname):
            sys.stderr.write('{} does not exist\n'.format(fname))
            sys.exit(-1)
        mc = pd.read_csv(fname, sep='\s+')

        # Get stats
        median = mc.median(axis=0)
        # std = mc.std(axis=0)
        lower_std = mc.quantile(q=0.16, axis=0)
        upper_std = mc.quantile(q=0.84, axis=0)
        # lower_std = mc.std(axis=0)
        # upper_std = mc.std(axis=0)

        for j in pd_keys:
            m = median[j]
            t = STATS[j]['true']
            s_l = median[j]-lower_std[j]
            s_u = upper_std[j]-median[j]
            if m > t:
                s = s_u
            else:
                s = s_l
            d = (m - t) / s

            STATS[j]['median'][i]=m
            STATS[j]['std'][i]=s
            STATS[j]['normdiff'][i]=d

            # sys.stderr.write('{}\t-- Median: {},\tstd: {},\td: {}\n'.format(j, m, s, d))


    # plot results
    plt.clf()
    plt.figure(1)

    bwidth=0.5

    plt.subplot(321)
    bins = make_bins(STATS['r0_thin']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['r0_thin']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    median = np.median(STATS['r0_thin']['normdiff'])
    # std = np.std(STATS['r0_thin']['normdiff'])
    std_minus = np.percentile(STATS['r0_thin']['normdiff'], q=16)
    std_plus = np.percentile(STATS['r0_thin']['normdiff'], q=84)
    # median_err = std/np.sqrt(Nfiles)
    median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    plt.axvline(median, color='r', linestyle='solid')
    # plt.axvline(median+std, color='r', linestyle='solid')
    # plt.axvline(median-std, color='r', linestyle='solid')
    # plt.axvline(median+median_err, color='r', linestyle='--')
    # plt.axvline(median-median_err, color='r', linestyle='--')
    plt.axvline(std_minus, color='r', linestyle='solid')
    plt.axvline(std_plus, color='r', linestyle='solid')
    plt.axvline(median - median_err_minus, color='r', linestyle='--')
    plt.axvline(median + median_err_plus, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{median-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($r_{0,thin}$)')

    plt.subplot(322)
    bins = make_bins(STATS['z0_thin']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['z0_thin']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    median = np.median(STATS['z0_thin']['normdiff'])
    # std = np.std(STATS['z0_thin']['normdiff'])
    std_minus = np.percentile(STATS['z0_thin']['normdiff'], q=16)
    std_plus = np.percentile(STATS['z0_thin']['normdiff'], q=84)
    # median_err = std/np.sqrt(Nfiles)
    median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    plt.axvline(median, color='r', linestyle='solid')
    # plt.axvline(median+std, color='r', linestyle='solid')
    # plt.axvline(median-std, color='r', linestyle='solid')
    # plt.axvline(median+median_err, color='r', linestyle='--')
    # plt.axvline(median-median_err, color='r', linestyle='--')
    plt.axvline(std_minus, color='r', linestyle='solid')
    plt.axvline(std_plus, color='r', linestyle='solid')
    plt.axvline(median - median_err_minus, color='r', linestyle='--')
    plt.axvline(median + median_err_plus, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{median-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($z_{0,thin}$)')

    plt.subplot(323)
    bins = make_bins(STATS['r0_thick']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['r0_thick']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    median = np.median(STATS['r0_thick']['normdiff'])
    # std = np.std(STATS['r0_thick']['normdiff'])
    std_minus = np.percentile(STATS['r0_thick']['normdiff'], q=16)
    std_plus = np.percentile(STATS['r0_thick']['normdiff'], q=84)
    # median_err = std/np.sqrt(Nfiles)
    median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    plt.axvline(median, color='r', linestyle='solid')
    # plt.axvline(median+std, color='r', linestyle='solid')
    # plt.axvline(median-std, color='r', linestyle='solid')
    # plt.axvline(median+median_err, color='r', linestyle='--')
    # plt.axvline(median-median_err, color='r', linestyle='--')
    plt.axvline(std_minus, color='r', linestyle='solid')
    plt.axvline(std_plus, color='r', linestyle='solid')
    plt.axvline(median - median_err_minus, color='r', linestyle='--')
    plt.axvline(median + median_err_plus, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{median-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($r_{0,thick}$)')

    plt.subplot(324)
    bins = make_bins(STATS['z0_thick']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['z0_thick']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    median = np.median(STATS['z0_thick']['normdiff'])
    # std = np.std(STATS['z0_thick']['normdiff'])
    std_minus = np.percentile(STATS['z0_thick']['normdiff'], q=16)
    std_plus = np.percentile(STATS['z0_thick']['normdiff'], q=84)
    # median_err = std/np.sqrt(Nfiles)
    median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    plt.axvline(median, color='r', linestyle='solid')
    # plt.axvline(median+std, color='r', linestyle='solid')
    # plt.axvline(median-std, color='r', linestyle='solid')
    # plt.axvline(median+median_err, color='r', linestyle='--')
    # plt.axvline(median-median_err, color='r', linestyle='--')
    plt.axvline(std_minus, color='r', linestyle='solid')
    plt.axvline(std_plus, color='r', linestyle='solid')
    plt.axvline(median - median_err_minus, color='r', linestyle='--')
    plt.axvline(median + median_err_plus, color='r', linestyle='--')
    plt.xlabel(r'$\frac{median-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($z_{0,thick}$)')

    plt.subplot(325)
    bins = make_bins(STATS['ratio']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['ratio']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    median = np.median(STATS['ratio']['normdiff'])
    # std = np.std(STATS['ratio']['normdiff'])
    std_minus = np.percentile(STATS['ratio']['normdiff'], q=16)
    std_plus = np.percentile(STATS['ratio']['normdiff'], q=84)
    # median_err = std/np.sqrt(Nfiles)
    median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    plt.axvline(median, color='r', linestyle='solid')
    # plt.axvline(median+std, color='r', linestyle='solid')
    # plt.axvline(median-std, color='r', linestyle='solid')
    # plt.axvline(median+median_err, color='r', linestyle='--')
    # plt.axvline(median-median_err, color='r', linestyle='--')
    plt.axvline(std_minus, color='r', linestyle='solid')
    plt.axvline(std_plus, color='r', linestyle='solid')
    plt.axvline(median - median_err_minus, color='r', linestyle='--')
    plt.axvline(median + median_err_plus, color='r', linestyle='--')
    plt.xlabel(r'$\frac{median-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($n_{0,thick}/n_{0,thin}$)')

    # plt.tight_layout()

    plt.savefig(data_dir + 'hist_100chains.png')



if __name__ == '__main__':
    main()
