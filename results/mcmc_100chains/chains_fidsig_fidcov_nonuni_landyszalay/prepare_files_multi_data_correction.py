'''
Prepares files to be read in to mcmc code. See ../mcmc_mpi/src/io.c for more
detail on what files we need.

Arguments:
    out_dir     - moving all data to this folder; mcmc will read from here only
    todo_dir    - contains todo_list (info about data)
    data_dir    - contains data samples which we'll use in chains
    model_dir   - MM points
    stats_dir   - contains mean and std files
    fid_dir     - contains inv correlation matrices
    bins_dir    - contains rbins
    Ndata       - number of data samples (usually 100)
'''
import sys, os
import numpy as np
import pandas as pd
from scipy import linalg

def main():

    # Parse CL
    elements_needed = int(10)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    out_dir   = args_array[1]
    todo_dir  = args_array[2]
    data_dir  = args_array[3]
    model_dir = args_array[4]
    mr_dir    = args_array[5]
    stats_dir = args_array[6]
    fid_dir   = args_array[7]
    bins_dir  = args_array[8]
    Ndata     = int(args_array[9])

    if not(os.path.isdir(out_dir)):
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    # Check that all passed directories exist and print them.
    for i in range(1, len(args_array)-1):
        if not(os.path.isdir(args_array[i])):
            sys.stderr.write('{} does not exist. Exiting...\n'.format(args_array[i]))
            sys.exit()
    sys.stderr.write('Output directory is {}\n'.format(out_dir))
    sys.stderr.write('Todo directory is {}\n'.format(todo_dir))
    sys.stderr.write('Data directory is {}\n'.format(data_dir))
    sys.stderr.write('Model directory is {}\n'.format(model_dir))
    sys.stderr.write('MR directory is {}\n'.format(mr_dir))
    sys.stderr.write('Stats directory is {}\n'.format(stats_dir))
    sys.stderr.write('Fiducial directory is {}\n'.format(fid_dir))
    sys.stderr.write('Bins directory is {}\n'.format(bins_dir))
    sys.stderr.write('{} data realizations.\n'.format(Ndata))

    # Make ID list from todo file
    todo_fname = todo_dir + 'todo_list.ascii.dat'
    ID = np.genfromtxt(todo_fname, usecols=[0], unpack=True, dtype=str, skip_header=1)
    out_fname = out_dir + 'pointing_ID.dat'
    with open(out_fname, 'w') as f:
        f.write(str(len(ID)))
        f.write('\n')
        for i in ID:
            f.write(i)
            f.write('\n')

    # Check for existence of bins files and load number of bins
    bins_fname = bins_dir + 'rbins.ascii.dat'
    if not(os.path.isfile(bins_fname)):
        sys.stderr.write('{} does not exist. Please make before continuing...\n'
                            .format(bins_fname))
        sys.exit()
    bins = np.genfromtxt(bins_fname, unpack=True, usecols=[0], skip_header=1)
    nbins = len(bins)

    # Also, copy bins file to out_dir
    cmd = 'cp ' + bins_fname + ' ' + out_dir
    os.system(cmd)

    # Prepare data for each l.o.s.
    for i in ID:

        if int(i) % 10 == 0:
            sys.stderr.write('Prep for pointing #{} of {} ..\n'.format(i, len(ID)))

        # make a list of pointings in which dd=0 occurs for one of the data samples
        # set flag = 1 for bad pointings
        bin_flags = np.zeros(nbins)
        for j in range(Ndata):
            tmp_dir = data_dir + 'sample_' + str(j) + '/'
            data_fname = tmp_dir + 'DDm2DR_' + i + '.dat'
            dd = np.genfromtxt(data_fname, skip_header=1)

            for k in range(nbins):
                if dd[k] == 0.0:
                    bin_flags[k] = 1

        # get dd counts
        for j in range(Ndata):
            tmp_dir = data_dir + 'sample_' + str(j) + '/'
            data_fname = tmp_dir + 'DDm2DR_' + i + '.dat'
            # First get number of randoms
            with open(data_fname, 'r') as f:
                firstline=f.readline()
                Nrand=int(firstline.strip()[1])
            dd = np.genfromtxt(data_fname, skip_header=1)
            dd = dd[np.where(bin_flags!=1)]

            out_fname = tmp_dir + 'ddm2dr_' + i + '.dat'
            with open(out_fname, 'w') as f:
                f.write('{}\t{}\n'.format(len(dd), Nrand))
                for d in dd:
                    f.write('{0:.6e}\n'.format(d))

        # get mean and standard deviation files
        stats_fname = stats_dir + 'mean_std_' + i + '.dat'
        mean_std = np.genfromtxt(stats_fname)
        mean_std = mean_std[np.where(bin_flags!=1)]
        out_fname = out_dir + 'mean_std_' + i + '.dat'
        np.savetxt(out_fname, mean_std, fmt='%.6e')

        # get inverse of correlation matrix
        corr_fname = fid_dir + 'correlation_' + i + '.dat'
        corr = pd.read_csv(corr_fname, sep='\s+', header=None)
        corr = corr.drop(np.where(bin_flags==1)[0],axis=0)
        corr = corr.drop(np.where(bin_flags==1)[0],axis=1)

        inv_corr = linalg.inv(corr.values)

        out_fname = out_dir + 'inv_correlation_' + i + '.dat'
        np.savetxt(out_fname, inv_corr, fmt='%.6e')

        # Copy and rename zrw file
        uni_fname = model_dir + 'uniform_' + i + '.ZRW.dat'
        nonuni_fname = model_dir + 'nonuniform_' + i + '.ZRW.dat'
        # Options: uniform or non-uniform file
        if(os.path.isfile(uni_fname)):
            model_fname = uni_fname
        elif(os.path.isfile(nonuni_fname)):
            model_fname = nonuni_fname
        else:
            sys.stderr.write('Error! Unrecognized model file. Exiting...\n')
            sys.exit()
        cmd = 'cp ' + model_fname + ' ' + out_dir + 'model_ZRW_' + i + '.dat'
        os.system(cmd)

        # Copy pair files
        k=0
        for j in range(nbins):
            if bin_flags[j]==1:
                continue
            pair_fname = model_dir + 'pair_indices_p' + i + '_b' + str(j) + '.dat'
            cmd = (
                'cp ' + pair_fname + ' ' + out_dir + 'MM_pair_indices_p' + i
                + '_b' + str(k) + '.dat'
                )
            os.system(cmd)
            k+=1

        k=0
        for j in range(nbins):
            if bin_flags[j]==1:
                continue
            pair_fname = mr_dir + 'pair_indices_p' + i + '_b' + str(j) + '.dat'
            cmd = (
                'cp ' + pair_fname + ' ' + out_dir + 'MR_pair_indices_p' + i
                + '_b' + str(k) + '.dat'
                )
            os.system(cmd)
            k+=1

    sys.stderr.write('The folder {} has all data ready to run an mcmc.\n'
                        .format(out_dir))

if __name__ == '__main__':
    main()