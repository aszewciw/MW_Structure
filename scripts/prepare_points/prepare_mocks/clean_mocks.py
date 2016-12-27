import numpy as np
import sys, os

#-----------------------------------------------------------------------------#
'''
Take mocks, which have unshuffled thin and thick disks upon creation, with more
stars than are in the corresponding line of sight. Shuffle mocks, cut out some
stars to produce files which contain the same number of stars as are in the
corresponding SEGUE l.o.s.
'''
#-----------------------------------------------------------------------------#

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

    # pass directory names and number of mocks
    min_args = int(3)
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert((N_args == min_args) or (N_args==min_args+1))
    todo_dir = args_array[1]
    out_dir = args_array[2]

    if(N_args==min_args):
        N_mocks = 2
        print('No number of mocks passed. Using default value of ' + str(N_mocks) )
    elif(N_args==min_args+1):
        N_mocks=int(args_array[3])
        print('Number of mocks: ' + str(N_mocks) )

    print('Randomly shuffling data and outputing different mock samples.\n')
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = todo_dir + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        ID_current = str(ID[i])
        N_data = N_stars[i]

        # Load position data for mock stars
        mock_file = out_dir + 'temp_mock_' + ID_current + '.xyzw.dat'
        xyzw = np.genfromtxt(mock_file)

        # Check that we have enough stars
        N_total = len(xyzw)
        diff = N_total - N_data*N_mocks
        if diff < 0:
            print("Oh no! We didn't make enough stars for " + ID_current)
            continue

        # Shuffle stars to mix disks; then assign to different mock realizations
        np.random.shuffle(xyzw)

        for j in range(N_mocks):
            key = str(j)
            samp_min = j*N_data
            samp_max = samp_min+N_data
            sample = xyzw[samp_min:samp_max]
            sample_dir = out_dir + 'sample_' + str(j) + '/'
            if not os.path.isdir(sample_dir):
                sys.stderr.write('{} does not exist Making directory...\n'.format(sample_dir))
                cmd = 'mkdir ' + sample_dir
                os.system(cmd)
            # Output new data
            out_file = sample_dir + 'mock_' + ID_current + '.xyzw.dat'
            np.savetxt(out_file, sample, fmt='%1.6f')
            # Add number of elements as first line in file
            line_prepender(out_file, str(int(N_data)))


    print('Data cleaned. Mocks written to {}\n'.format(out_dir))

if __name__ == '__main__':
    main()