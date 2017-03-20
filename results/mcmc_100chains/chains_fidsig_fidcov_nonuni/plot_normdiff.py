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


def make_bins(x, bwidth):

    bin_min=int(min(x))-1
    bin_max=int(max(x))+1+bwidth

    bins=np.arange(bin_min,bin_max,bwidth)

    return bins


def main():

    # Optional cl input
    # Pass any files that we wish to exclude
    args_array = np.array(sys.argv)
    Nskip = len(args_array)-1
    sys.stderr.write('Not including data for {} files.\n'.format(Nskip))

    bad_files = []
    for i in range(Nskip):
        j = int(args_array[i+1])
        bad_files.append(j)
        sys.stderr.write('Skipping file {} \n'.format(j))

    Nfiles=100 - Nskip

    stats_fname='./out_data/normdiff_100chains.dat'
    if not os.path.isfile(stats_fname):
        sys.stderr.write('Error: {} does not exist.\n')

    # Make a dictionary to store statistics calculated for each chain
    pd_keys=['r0_thin', 'z0_thin', 'r0_thick', 'z0_thick', 'ratio', 'chi2']
    # labels=[r'$r_{0,thin}$', r'$z_{0,thin}$', r'$r_{0,thick}$', r'$z_{0,thick}$', r'$n_{0,thick}/n_{0,thin}$', r'min($\chi^2$)']
    labels=[r'$r_0$, thick', r'$z_0$, thin', r'$r_0$, thick', r'$z_0$, thick', 'a', r'min($\chi^2$)']
    STATS={}

    # Load each column of the file into this dictionary
    for i in range(len(pd_keys)):
        key = pd_keys[i]
        STATS[key]={}
        # (true-median)/std
        STATS[key]['normdiff']=np.genfromtxt(stats_fname, unpack=True, usecols=i)

    axis_label = r'$\frac{true-median}{\sigma}$'

    # plot results
    plt.clf()
    plt.figure(1)

    bwidth=0.5
    spnum = 321

    # for i in range(len(pd_keys)):
    #     key = pd_keys[i]
    #     if key=='chi2':
    #         continue
    #     plt.subplot(spnum+i)
    #     bins = make_bins(STATS[key]['normdiff'], bwidth)
    #     n, b, patches = plt.hist(STATS[key]['normdiff'], bins=bins,
    #         facecolor='green', alpha=0.7, label=labels[i])
    #     median = np.median(STATS[key]['normdiff'])
    #     std_minus = np.percentile(STATS[key]['normdiff'], q=16)
    #     std_plus = np.percentile(STATS[key]['normdiff'], q=84)
    #     median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    #     median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    #     med_label = 'med='+str(np.round(median,2))
    #     std_plt = np.round((std_plus-std_minus)/2.0, 2)
    #     std_label = r'$\sigma$='+str(std_plt)
    #     plt.axvline(median, color='r', linestyle='solid', label=med_label)
    #     plt.axvline(std_minus, color='b', linestyle='solid', label=std_label)
    #     plt.axvline(std_plus, color='b', linestyle='solid')
    #     plt.axvline(median - median_err_minus, color='r', linestyle='--')
    #     plt.axvline(median + median_err_plus, color='r', linestyle='--')
    #     plt.axis([min(bins), max(bins), 0, 1.1*max(n)])
    #     # plt.ylabel(labels[i])
    #     if i==3 or i==4:
    #         plt.xlabel(axis_label, fontsize=12)
    #     # Decide where to place legend
    #     left = median - np.min(STATS[key]['normdiff'])
    #     right = np.max(STATS[key]['normdiff']) - median
    #     if left>right:
    #         loc='upper left'
    #     else:
    #         loc='upper right'
    #     plt.legend(loc=loc, fontsize=6)
    #     sys.stderr.write('Key: {}, min: {}, max: {}\n'.format(key, np.min(STATS[key]['normdiff']), np.max(STATS[key]['normdiff']) ) )

    # plt.savefig(data_dir + 'normdiff' + '.png')





    for i in range(len(pd_keys)):
        key = pd_keys[i]
        if key=='chi2':
            bwidth = 20
        else:
            bwdith = 0.5
        plt.subplot(spnum+i)
        bins = make_bins(STATS[key]['normdiff'], bwidth)
        n, b, patches = plt.hist(STATS[key]['normdiff'], bins=bins,
            facecolor='green', alpha=0.7, label=labels[i])
        median = np.median(STATS[key]['normdiff'])
        std_minus = np.percentile(STATS[key]['normdiff'], q=16)
        std_plus = np.percentile(STATS[key]['normdiff'], q=84)
        median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
        median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
        med_label = 'med='+str(np.round(median,2))
        std_plt = np.round((std_plus-std_minus)/2.0, 2)
        std_label = r'$\sigma$='+str(std_plt)
        plt.axvline(median, color='r', linestyle='solid', label=med_label)
        plt.axvline(std_minus, color='b', linestyle='solid', label=std_label)
        plt.axvline(std_plus, color='b', linestyle='solid')
        plt.axvline(median - median_err_minus, color='r', linestyle='--')
        plt.axvline(median + median_err_plus, color='r', linestyle='--')
        plt.axis([min(bins), max(bins), 0, 1.1*max(n)])
        if i==3 or i==5:
            plt.xlabel(axis_label, fontsize=12)
        # Decide where to place legend
        left = median - np.min(STATS[key]['normdiff'])
        right = np.max(STATS[key]['normdiff']) - median
        if left>right:
            loc='upper left'
        else:
            loc='upper right'
        plt.legend(loc=loc, fontsize=6)
        sys.stderr.write('Key: {}, min: {}, max: {}\n'.format(key, np.min(STATS[key]['normdiff']), np.max(STATS[key]['normdiff']) ) )

    plt.savefig(data_dir + 'normdiff' + '.png')


if __name__ == '__main__':
    main()
