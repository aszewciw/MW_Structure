'''
Loops over all SEGUE los and produces a file for each bin (12)
in each los (152) containing the indices of pairs in a uniform
sample with same geometry as that los.
'''

from config import *

## ------------------------------------------------------------------------- ##

def line_prepender(filename, line):
    '''
    Appends a line to the beginning of a file.

    Arguments:
    1. filename : (str) name of file
    2. line : (str) line to be appended
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

## ------------------------------------------------------------------------- ##

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    bin_lower, bin_upper = np.genfromtxt(bins_file, skip_header=1,
        unpack=True, usecols=[0, 1])

    Nbins = len(bin_lower)

    for p in todo_list:

        in_file = uni_dir + 'uniform_' + p.ID + '.xyz.dat'
        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        # Count pairs in each bin
        for i in range(Nbins):

            param = str(bin_lower[i]) + ' ' + str(bin_upper[i])
            output_file = ( pairs_dir + 'counts_' + p.ID + '.bin_' + str(i)
                + '.dat' )
            cmd = ( './uni_pair_count ' + in_file + ' ' + param + ' > '
                + output_file )
            os.system(cmd)

            # prepend length of array to file
            indexes = np.genfromtxt(output_file)
            length = str(len(indexes))
            line_prepender(output_file, length)

if __name__ == '__main__':
    main()