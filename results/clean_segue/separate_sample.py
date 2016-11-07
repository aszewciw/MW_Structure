#!/usr/bin/env python

import mw_utilities_python as mwu
import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string

#------------------------------------------------------------------------------
def main():

    cleaned_dir = mwu.get_path.get_cleandata_path()

    # read pickled G star sample
    input_filename = cleaned_dir + 'gstar_sample.dat'
    sys.stderr.write('Reading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    gstar_list = pickle.load(input_file)
    input_file.close()

    # load pointing list
    input_filename = cleaned_dir + 'pointing_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    pointing_list = pickle.load(input_file)
    input_file.close()

    # the cos of the plate size
    plate_size_cos = math.cos(seg.PLATE_RADIUS_RADIANS)

    # For each star in the photometric sample, check which pointing it belongs
    # to, and assign the corresponding pointing ID to it.
    status_count = 0

    for p in pointing_list:
        p.star_list = []

    # use dot product to check
    for s in gstar_list:
        for p in pointing_list:
            # get star's Cartesian coordinates on the unit sphere
            s_xyz = seg.eq2cart(s.ra_rad, s.dec_rad, 1.0)
            p_xyz = (p.cartesian_x, p.cartesian_y, p.cartesian_z)
            if seg.dot(s_xyz, p_xyz) >= plate_size_cos:
                s.pointingID = p.ID
                p.star_list.append(s)
                break

        status_count += 1

        if status_count % (int(len(gstar_list)/10)) == 0:
            sys.stderr.write("Checking particle #{0}\n"
                             .format(status_count))

    sys.stderr.write('Start splitting files...\n')

    # open files and output for each pointing:
    for p in pointing_list:

        if len(p.star_list) == 0:
            continue # skip empty or very few stars pointing

        output_filename = cleaned_dir + 'gstar_' + p.ID + '.dat'
        output_file = open(output_filename, 'wb')
        pickle.dump(p.star_list, output_file)
        output_file.close()


    sys.stderr.write("Done splitting files.\n")

if __name__ == '__main__':
    main()

