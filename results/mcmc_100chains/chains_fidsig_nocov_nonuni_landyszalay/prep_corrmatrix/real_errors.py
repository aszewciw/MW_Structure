import pandas as pd
from scipy import linalg
import numpy as np
import sys, os

#------------------------------------------------------------------------------#
'''
Load weighted and normalized pair counts for Nmocks. Output the following files
(one per los):

1. normed_counts_all - contains an Nmocks by Nbins list of all weighted and
    normalized dd counts.
2. mean_std - contains the mean and standard deviation of pair counts across all
    Nmocks
3. correlation - contains correlation matrix for these Nmocks mocks
4. inv_correlation - contains inverse of corr matrix for Nmocks mocks
'''
#------------------------------------------------------------------------------#

def main():

    # Parse CL
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    todo_dir  = args_array[1]
    pairs_dir = args_array[2]
    out_dir   = args_array[3]
    Nmocks    = int(args_array[4])

    # Load list of pointing IDs
    todo_file = todo_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Get number of bins by loading one pair counts file
    N_bins = 12

    # Create a file containing all normed counts
    for ID in ID_list:

        dd_all = np.zeros((Nmocks, N_bins))

        # loop over all mocks
        for i in range(Nmocks):

            # Load counts for a single mock
            counts_file = pairs_dir + 'sample_' + str(i) + '/DDm2DR_' + ID + '.dat'
            dd_all[i] = np.genfromtxt( counts_file, dtype=float )

        # Output data
        output_filename = out_dir + 'normed_counts_all_' + ID + '.dat'
        np.savetxt(output_filename, dd_all, fmt='%.6e')

        sys.stderr.write('Calculating correlation for pointing {}\n'.format(ID))

        # Load normalized counts
        # Each row is a mock, each column is a bin
        counts_filename = out_dir + 'normed_counts_all_' + ID + '.dat'
        DD = pd.read_csv(counts_filename, sep='\s+', header=None)

        # Calculate correlation matrix
        corr = DD.corr().values

        out_file = out_dir + 'correlation_' + ID + '.dat'
        np.savetxt(out_file, corr, fmt='%.6e')

        # Invert covariance matrix and save to file
        inv_corr = linalg.inv(corr)

        out_file = out_dir + 'inv_correlation_' + ID + '.dat'
        np.savetxt(out_file, inv_corr, fmt='%.6e')

        # Last calculate mean & std and save to file
        mean = DD.mean(axis=0).values
        std  = DD.std(axis=0).values
        mean_std = np.column_stack((mean,std))

        out_file = out_dir + 'mean_std_' + ID + '.dat'
        np.savetxt(out_file, mean_std, fmt='%.6e')

if __name__ == '__main__':
    main()