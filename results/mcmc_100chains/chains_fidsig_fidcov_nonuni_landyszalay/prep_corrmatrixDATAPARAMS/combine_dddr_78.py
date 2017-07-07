'''
Produce files containing the indices of binned pairs. Here we do this for a
uniform sample.
'''
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    Nmocks = 1000
    star_factor = 10
    dd_dir = '../../prep_fid_errors_DATAPARAMS/data/'
    dr_dir = './data/'
    out_dir = './data/'

    # get directories of scripts, executables, and star files
    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(out_dir))
        sys.exit(1)

    if not os.path.isdir(dr_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(dr_dir))
        sys.exit(1)

    if not os.path.isdir(dd_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(dd_dir))
        sys.exit(1)

    # Load todo list
    input_filename = cleaned_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Write command file
    for i in range(Nmocks):

        if i <700: continue
        if i>799: continue

        sys.stderr.write('On sample {}/{}\n'.format(i,Nmocks))
        DD_dir  = dd_dir + 'sample_' + str(i) + '/'

        DR_dir  = dr_dir + 'sample_' + str(i) + '/'

        OUT_dir = out_dir + 'sample_' + str(i) + '/'

        if not os.path.isdir(DD_dir):
            sys.stderr.write('{} does not exist. Exiting...\n'.format(DD_dir))
            sys.exit(1)

        if not os.path.isdir(DR_dir):
            sys.stderr.write('{} does not exist. Exiting...\n'.format(DR_dir))
            sys.exit(1)

        if not os.path.isdir(OUT_dir):
            sys.stderr.write('{} does not exist. Exiting...\n'.format(OUT_dir))
            sys.exit(1)

        for p in todo_list:

            N_rand = int(p.N_star * star_factor)

            dr_file  = DR_dir + 'dr_' + p.ID + '.dat'
            dd_file  = DD_dir + 'dd_' + p.ID + '.dat'
            out_file = OUT_dir + 'DDm2DR_' + p.ID + '.dat'

            dr = np.genfromtxt(dr_file, unpack=True, usecols=[4])
            dd = np.genfromtxt(dd_file, unpack=True, usecols=[4])

            ddm2dr = dd - 2.0*dr

            np.savetxt(out_file, ddm2dr, fmt='%.6e')

if __name__ == '__main__':
    main()