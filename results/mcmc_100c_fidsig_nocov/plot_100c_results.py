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


    # plot results
    plt.clf()
    plt.figure(1)

    plt.subplot(321)
    n, bins, patches = plt.hist(STATS['r0_thin']['normdiff'], 10, facecolor='green', alpha=0.7)
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.title(r'$r_{0,thin}$', fontsize=16)

    plt.subplot(322)
    n, bins, patches = plt.hist(STATS['z0_thin']['normdiff'], 10, facecolor='green', alpha=0.7)
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.title(r'$z_{0,thin}$', fontsize=16)

    plt.subplot(323)
    n, bins, patches = plt.hist(STATS['r0_thick']['normdiff'], 10, facecolor='green', alpha=0.7)
    # plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.title(r'$r_{0,thick}$', fontsize=16)

    plt.subplot(324)
    n, bins, patches = plt.hist(STATS['z0_thick']['normdiff'], 10, facecolor='green', alpha=0.7)
    plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.title(r'$z_{0,thick}$', fontsize=16)

    plt.subplot(325)
    n, bins, patches = plt.hist(STATS['z0_thick']['normdiff'], 10, facecolor='green', alpha=0.7)
    plt.xlabel(r'$\frac{mean-true}{\sigma}$', fontsize=16)
    plt.title(r'$n_{0,thick}/n_{0,thin}$', fontsize=16)

    # plt.tight_layout()

    plt.savefig('hist_100chains.png')

if __name__ == '__main__':
    main()
