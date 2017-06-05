import numpy as np
import sys, os



def main():

    max_plist = 164
    nsamps = 100
    nbins = 12

    for p in range(max_plist):
        ID = str(p)

        if not os.path.isfile('./data/sample_0/DD_{}.dat'.format(ID)):
            sys.stderr.write('Pointing {} does not exist.\n'.format(ID))
            continue

        nzeros = np.zeros(nbins)

        for samp in range(nsamps):

            dd = np.genfromtxt('./data/sample_{}/DD_{}.dat'.format(samp, ID))

            for i in range(nbins):

                if dd[i]==0.0:
                    nzeros[i] += 1


        print('Pointing {}: {}'.format(ID, nzeros))


if __name__ == '__main__':
    main()