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
        # Distribution mean and standard deviation
        STATS[i]['mean']=np.zeros(Nfiles)
        STATS[i]['std']=np.zeros(Nfiles)
        # (mean-true)/std
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
        mean = mc.mean(axis=0)
        std = mc.std(axis=0)

        for j in pd_keys:
            m = mean[j]
            s = std[j]
            t = STATS[j]['true']
            d = (m - t) / s

            STATS[j]['mean'][i]=m
            STATS[j]['std'][i]=s
            STATS[j]['normdiff'][i]=d


    nd_stats = {}

    # plot results
    plt.clf()
    plt.figure(1)

    bwidth=0.5

    plt.subplot(321)
    bins = make_bins(STATS['r0_thin']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['r0_thin']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    mean = np.mean(STATS['r0_thin']['normdiff'])
    std = np.std(STATS['r0_thin']['normdiff'])
    mean_err = std/np.sqrt(Nfiles)
    plt.axvline(mean, color='r', linestyle='solid')
    plt.axvline(mean+std, color='r', linestyle='solid')
    plt.axvline(mean-std, color='r', linestyle='solid')
    plt.axvline(mean+mean_err, color='r', linestyle='--')
    plt.axvline(mean-mean_err, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($r_{0,thin}$)')

    plt.subplot(322)
    bins = make_bins(STATS['z0_thin']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['z0_thin']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    mean = np.mean(STATS['z0_thin']['normdiff'])
    std = np.std(STATS['z0_thin']['normdiff'])
    mean_err = std/np.sqrt(Nfiles)
    plt.axvline(mean, color='r', linestyle='solid')
    plt.axvline(mean+std, color='r', linestyle='solid')
    plt.axvline(mean-std, color='r', linestyle='solid')
    plt.axvline(mean+mean_err, color='r', linestyle='--')
    plt.axvline(mean-mean_err, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($z_{0,thin}$)')

    plt.subplot(323)
    bins = make_bins(STATS['r0_thick']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['r0_thick']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    mean = np.mean(STATS['r0_thick']['normdiff'])
    std = np.std(STATS['r0_thick']['normdiff'])
    mean_err = std/np.sqrt(Nfiles)
    plt.axvline(mean, color='r', linestyle='solid')
    plt.axvline(mean+std, color='r', linestyle='solid')
    plt.axvline(mean-std, color='r', linestyle='solid')
    plt.axvline(mean+mean_err, color='r', linestyle='--')
    plt.axvline(mean-mean_err, color='r', linestyle='--')
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($r_{0,thick}$)')

    plt.subplot(324)
    bins = make_bins(STATS['z0_thick']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['z0_thick']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    mean = np.mean(STATS['z0_thick']['normdiff'])
    std = np.std(STATS['z0_thick']['normdiff'])
    mean_err = std/np.sqrt(Nfiles)
    plt.axvline(mean, color='r', linestyle='solid')
    plt.axvline(mean+std, color='r', linestyle='solid')
    plt.axvline(mean-std, color='r', linestyle='solid')
    plt.axvline(mean+mean_err, color='r', linestyle='--')
    plt.axvline(mean-mean_err, color='r', linestyle='--')
    plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($z_{0,thick}$)')

    plt.subplot(325)
    bins = make_bins(STATS['ratio']['normdiff'], bwidth)
    n, b, patches = plt.hist(STATS['ratio']['normdiff'], bins=bins, facecolor='green', alpha=0.7)
    mean = np.mean(STATS['ratio']['normdiff'])
    std = np.std(STATS['ratio']['normdiff'])
    mean_err = std/np.sqrt(Nfiles)
    plt.axvline(mean, color='r', linestyle='solid')
    plt.axvline(mean+std, color='r', linestyle='solid')
    plt.axvline(mean-std, color='r', linestyle='solid')
    plt.axvline(mean+mean_err, color='r', linestyle='--')
    plt.axvline(mean-mean_err, color='r', linestyle='--')
    plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.ylabel(r'N ($n_{0,thick}/n_{0,thin}$)')

    # plt.tight_layout()

    plt.savefig('hist_100chains.png')



if __name__ == '__main__':
    main()
