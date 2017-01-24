import numpy as np
import sys
import mw_utilities_python.segue_star as seg

#-----------------------------------------------------------------------------#
'''
Take mocks, which have unshuffled thin and thick disks upon creation, with more
stars than are in the corresponding line of sight. Shuffle mocks, cut out some
stars to produce files which contain the same number of stars as are in the
corresponding SEGUE l.o.s.
'''
#-----------------------------------------------------------------------------#

## ------------------------------------------------------------------------- ##

def main():

    # pass directory names
    elements_needed = int(3)
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    todo_dir = args_array[1]
    out_dir  = args_array[2]

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

        # Load xyzw
        in_file = out_dir + 'nonuniform_' + ID_current + '.xyzw.dat'
        x,y,z,w = np.genfromtxt(in_file, skip_header=1, unpack=True)

        Nstars = len(x)

        Z = np.zeros(Nstars)
        R = np.zeros(Nstars)

        for i in range(Nstars):
            ra, dec, r = seg.cart2eq(x[i], y[i], z[i])
            l, b = seg.eq2gal(ra, dec)
            Z[i], R[i] = seg.gal2ZR(l, b, r)

        out_file = out_dir + 'nonuniform_' + ID_current + '.ZRW.dat'
        with open(out_file, "w") as f:
            f.write('{}\n'.format(Nstars))
            for i in range(Nstars):
                f.write('{0:.6e}\t{1:.6e}\t{2:.6e}\n'.format(Z[i], R[i], w[i]))

    print('Data cleaned. Mocks written to {}\n'.format(out_dir))

if __name__ == '__main__':
    main()