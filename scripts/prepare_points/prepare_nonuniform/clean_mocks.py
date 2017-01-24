import numpy as np
import sys

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

    # pass directory names
    elements_needed = int(4)
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    todo_dir = args_array[1]
    out_dir  = args_array[2]
    star_factor = int(args_array[3])

    print('Mocks have too many stars. Randomly removing some.\n')
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = todo_dir + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        ID_current = str(ID[i])
        N_data = N_stars[i]*star_factor

        # Load position data for mock stars
        mock_file = out_dir + 'temp_mock_' + ID_current + '.xyzw.dat'
        xyz = np.genfromtxt(mock_file)

        # Randomly cut from mock sample to make it size of SEGUE data
        N_mock = len(xyz)
        diff = N_mock - N_data
        if diff < 0:
            print("Oh no! We didn't make enough stars for " + ID_current)
            continue
        delete_me = np.arange(diff)
        np.random.shuffle(xyz)
        xyz = np.delete(xyz, delete_me, 0)
        if N_data != len(xyz):
            print("Something went wrong! Incorrect number of stars for " + ID_current)
            continue

        # Output new data
        out_file = out_dir + 'nonuniform_' + ID_current + '.xyzw.dat'
        np.savetxt(out_file, xyz, fmt='%1.6e')

        # Add number of elements as first line in file
        line_prepender(out_file, str(int(N_data)))

    print('Data cleaned. Mocks written to {}\n'.format(out_dir))

if __name__ == '__main__':
    main()