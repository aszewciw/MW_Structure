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
    data_dir='./out_data/'

    # Make a dictionary to store statistics calculated for each chain
    pd_keys=['r0_thin', 'z0_thin', 'r0_thick', 'z0_thick', 'ratio']
    labels=[r'N ($r_{0,thin}$)', r'N ($z_{0,thin}$)', r'N ($r_{0,thick}$)', r'N ($z_{0,thick}$)', r'N ($n_{0,thick}/n_{0,thin}$)']
    STATS={}
    for i in pd_keys:
        STATS[i]={}
        # Distribution median and standard deviation
        STATS[i]['median']=np.zeros(Nfiles)
        STATS[i]['std']=np.zeros(Nfiles)
        # (true-median)/std
        STATS[i]['normdiff']=np.zeros(Nfiles)

    STATS['r0_thin']['true']=2.027
    STATS['z0_thin']['true']=0.234
    STATS['r0_thick']['true']=2.397
    STATS['z0_thick']['true']=0.675
    STATS['ratio']['true']=0.053

    best_chi2 = np.zeros(Nfiles)

    # Load results of each chain and compute stats
    k = 0
    for i in range(100):
        if (i in bad_files):
            continue
        if(i%10==0):
            sys.stderr.write('On result #{} of {}\n'.format(i,100))
        fname = data_dir + 'results_' + str(i) + '.dat'
        if not os.path.isfile(fname):
            sys.stderr.write('{} does not exist\n'.format(fname))
            sys.exit(-1)
        mc = pd.read_csv(fname, sep='\s+')

        # Get stats
        median = mc.median(axis=0)
        lower_std = mc.quantile(q=0.16, axis=0)
        upper_std = mc.quantile(q=0.84, axis=0)


        for j in pd_keys:
            m = median[j]
            t = STATS[j]['true']
            s_l = median[j]-lower_std[j]
            s_u = upper_std[j]-median[j]
            if t < m:
                s = s_l
            else:
                s = s_u
            d = (t - m) / s

            STATS[j]['median'][k]=m
            STATS[j]['std'][k]=s
            STATS[j]['normdiff'][k]=d

        best_chi2[k] = min(mc['chi2'])
        k+=1


    stats_fname = data_dir + 'normdiff_100chains.dat'
    with open(stats_fname, 'w') as f:
        # Write keys as first line
        f.write('# ')
        for i in pd_keys:
            f.write('{}\t'.format(i))
        f.write('best_chi2\n')

        for i in range(Nfiles):
            for j in pd_keys:
                f.write('{}\t'.format(STATS[j]['normdiff'][i]))
            f.write('{}\n'.format(best_chi2[i]))

    stats_fname = data_dir + 'stds_100chains.dat'
    with open(stats_fname, 'w') as f:
        # Write keys as first line
        f.write('# ')
        for i in pd_keys:
            f.write('{}\t'.format(i))
        f.write('best_chi2\n')

        for i in range(Nfiles):
            for j in pd_keys:
                f.write('{}\t'.format(STATS[j]['std'][i]))
            f.write('{}\n'.format(best_chi2[i]))

    stats_fname = data_dir + 'medians_100chains.dat'
    with open(stats_fname, 'w') as f:
        # Write keys as first line
        f.write('# ')
        for i in pd_keys:
            f.write('{}\t'.format(i))
        f.write('best_chi2\n')

        for i in range(Nfiles):
            for j in pd_keys:
                f.write('{}\t'.format(STATS[j]['median'][i]))
            f.write('{}\n'.format(best_chi2[i]))


    # # These don't really work because of binning

    # # stats_type = 'std'
    # # stats_type = 'median'
    # stats_type = 'normdiff'

    # if stats_type == 'std':
    #     axis_label = 'std'
    # elif stats_type == 'median':
    #     axis_label = 'median'
    # elif stats_type == 'normdiff':
    #     axis_label = r'$\frac{true-median}{\sigma}$'


    # # plot results
    # plt.clf()
    # plt.figure(1)

    # # this is a good bin width for normdiff, but it doesn't work for the others
    # bwidth=0.5

    # spnum = 321

    # for i in range(len(pd_keys)):
    #     key = pd_keys[i]
    #     plt.subplot(spnum+i)
    #     bins = make_bins(STATS[key][stats_type], bwidth)
    #     n, b, patches = plt.hist(STATS[key][stats_type], bins=bins, facecolor='green', alpha=0.7)
    #     median = np.median(STATS[key][stats_type])
    #     std_minus = np.percentile(STATS[key][stats_type], q=16)
    #     std_plus = np.percentile(STATS[key][stats_type], q=84)
    #     median_err_minus = (median-std_minus)/np.sqrt(Nfiles)
    #     median_err_plus = (std_plus-median)/np.sqrt(Nfiles)
    #     med_label = 'med='+str(np.round(median,2))
    #     std_plt = np.round((std_plus-std_minus)/2.0, 2)
    #     std_label = r'$\sigma$='+str(std_plt)
    #     plt.axvline(median, color='r', linestyle='solid', label=med_label)
    #     plt.axvline(std_minus, color='r', linestyle='solid', label=std_label)
    #     plt.axvline(std_plus, color='r', linestyle='solid')
    #     plt.axvline(median - median_err_minus, color='r', linestyle='--')
    #     plt.axvline(median + median_err_plus, color='r', linestyle='--')
    #     plt.ylabel(labels[i])
    #     if i==3 or i==4:
    #         plt.xlabel(axis_label, fontsize=16)
    #     plt.legend(loc='upper right')
    #     std_median = np.median(STATS[key]['std'])
    #     sys.stderr.write('Median standard deviation for {} is {}\n'.format(key,std_median))

    # # plt.tight_layout()
    # plt.savefig(data_dir + stats_type + '.png')


if __name__ == '__main__':
    main()
