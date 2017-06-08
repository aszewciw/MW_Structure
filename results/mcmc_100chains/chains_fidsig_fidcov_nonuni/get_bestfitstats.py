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
        # STATS[i]['std']=np.zeros(Nfiles)
        # # (true-best)/std
        # STATS[i]['normdiff']=np.zeros(Nfiles)
        STATS[i]['bestfit'] = np.zeros(Nfiles)

    STATS['r0_thin']['true']=2.027
    STATS['z0_thin']['true']=0.234
    STATS['r0_thick']['true']=2.397
    STATS['z0_thick']['true']=0.675
    STATS['ratio']['true']=0.053

    best_chi2 = np.zeros(Nfiles)
    truth_chi2 = np.zeros(Nfiles)

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
        # median = mc.idxmin(axis=0)
        # lower_std = mc.quantile(q=0.16, axis=0)
        # upper_std = mc.quantile(q=0.84, axis=0)
        min_ind = mc.idxmin(axis=0)['chi2']

        for j in pd_keys:
            # m = median[j]
            # t = STATS[j]['true']
            # s_l = median[j]-lower_std[j]
            # s_u = upper_std[j]-median[j]
            # if t < m:
            #     s = s_l
            # else:
            #     s = s_u
            # d = (t - m) / s

            # STATS[j]['median'][k]=m
            # STATS[j]['std'][k]=s
            # STATS[j]['normdiff'][k]=d
            STATS[j]['bestfit'][k] = mc[j][min_ind]

        best_chi2[k] = mc['chi2'][min_ind]
        truth_chi2[k] = mc['chi2'][0]
        k+=1


    stats_fname = data_dir + 'bestparams_100chains.dat'
    with open(stats_fname, 'w') as f:
        # Write keys as first line
        f.write('# ')
        for i in pd_keys:
            f.write('{}\t'.format(i))
        f.write('best_chi2\ttruth_chi2\n')

        for i in range(Nfiles):
            for j in pd_keys:
                f.write('{}\t'.format(STATS[j]['bestfit'][i]))
            f.write('{}\t{}\n'.format(best_chi2[i], truth_chi2[i]))

if __name__ == '__main__':
    main()
