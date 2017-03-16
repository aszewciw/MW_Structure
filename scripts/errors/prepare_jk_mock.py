'''
for an xyzw file, create jackknife samples for pair counting
'''

import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string, random
import numpy as np

#--------------------------------------------------------------------------

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

#--------------------------------------------------------------------------
def main():

    # Parse CL
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    N_jackknife = int(args_array[1])
    todo_dir    = args_array[2]
    file_dir    = args_array[3]
    out_dir     = args_array[4]

    if not(os.path.isdir(out_dir)):
        sys.stderr.write('{} does not exist. Making...\n'.format(out_dir))
        cmd='mkdir ' + out_dir
        os.system(cmd)

    # load the todo pointing list
    input_filename = todo_dir + 'todo_list.dat'
    if not(os.path.isfile(input_filename)):
        sys.write('Error: {} does not exist. Exiting...\n'.format(input_filename))
        sys.exit()
    sys.stderr.write('Loading pointing info from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Jackknifing mocks from {}\n'.format(file_dir))

    for p in todo_list:

        # Mocks are random upon creation so no need to shuffle
        filename = file_dir + 'mock_' + p.ID + '.xyzw.dat'
        if not(os.path.isfile(filename)):
            sys.write('Error: {} does not exist. Exiting...\n'.format(filename))
            sys.exit()
        xyzw = np.genfromtxt( filename, skip_header=1 )

        # jackknife samples
        N_uni = len( xyzw )
        remain = N_uni % N_jackknife

        for i in range( N_jackknife ):

            # Make every sub-sample the same size
            slice_length = int(N_uni / N_jackknife)
            lower_ind = i * slice_length
            upper_ind = lower_ind + slice_length
            remove_me = np.arange(lower_ind, upper_ind, 1)

            # Remove slice
            xyzw_temp = np.delete(xyzw, remove_me, 0)
            N_temp = len(xyzw_temp)

            # Output jackknife'd file
            out_file = out_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.dat'
            np.savetxt(out_file, xyzw_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(N_temp))

    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(out_dir))


if __name__ == '__main__' :
    main()
