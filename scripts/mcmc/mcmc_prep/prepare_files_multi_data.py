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

def main():

    # Parse CL
    elements_needed = int(9)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    out_dir   = args_array[1]
    todo_dir  = args_array[2]
    data_dir  = args_array[3]
    model_dir = args_array[4]
    stats_dir = args_array[5]
    fid_dir   = args_array[6]
    bins_dir  = args_array[7]
    Ndata     = int(args_array[8])

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

        # get dd counts
        for j in range(Ndata):
            tmp_dir = data_dir + 'sample_' + str(j) + '/'
            data_fname = tmp_dir + 'dd_' + i + '.dat'
            dd = np.genfromtxt(data_fname, usecols=[4], unpack=True, skip_header=1)
            out_fname = tmp_dir + 'DD_' + i + '.dat'
            with open(out_fname, 'w') as f:
                for d in dd:
                    f.write('{0:.6e}\n'.format(d))

        # get mean and standard deviation files
        # stats_fname = stats_dir + 'stats_' + i + '.dat'
        # mean, std = np.genfromtxt(stats_fname, usecols=[0,2], unpack=True)
        # out_fname = out_dir + 'mean_std_' + i + '.dat'
        # with open(out_fname, 'w') as f:
        #     for j in range(len(mean)):
        #         f.write('{0:.6e}\t{1:.6e}\n'.format(mean[j], std[j]))
        stats_fname = stats_dir + 'mean_std_' + i + '.dat'
        cmd = 'cp ' + stats_fname + ' ' + out_dir + 'mean_std_' + i + '.dat'
        os.system(cmd)

        # copy inverse correlation matrix files
        corr_fname = fid_dir + 'inv_correlation_' + i + '.dat'
        cmd = 'cp ' + corr_fname + ' ' + out_dir + 'inv_correlation_' + i + '.dat'
        os.system(cmd)

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
        for j in range(nbins):
            pair_fname = model_dir + 'pair_indices_p' + i + '_b' + str(j) + '.dat'
            cmd = 'cp ' + pair_fname + ' ' + out_dir
            os.system(cmd)


    sys.stderr.write('The folder {} has all data ready to run an mcmc.\n'
                        .format(out_dir))

if __name__ == '__main__':
    main()