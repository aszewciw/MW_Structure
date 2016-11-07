import mw_utilities_python as mwu
import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string

def main():

    # Get paths
    rawdata_dir = mwu.get_path.get_rawdata_path()
    cleaned_dir = mwu.get_path.get_cleandata_path()

    star_list = []

    # read the original data file
    input_filename = rawdata_dir + 'raw_data.dat'
    sys.stderr.write('Reading from input file {} ...\n'.format(input_filename))
    in_file = open(input_filename, 'r')

    for line in in_file:
        if line.lstrip().startswith('#'):
            continue
        s = seg.Star()

        record = line.split()
        # add an empty element at the beginning of the list,
        # so that the following index matches the column number.
        record.insert(0, '')

        s.sspecobjid = record[1]
        s.sobjid     = record[2]
        s.spplate    = record[3]
        s.rv         = float(record[4])
        s.rverr      = float(record[5])
        s.r0         = float(record[6])
        s.g0         = float(record[7])
        s.feha       = float(record[8])
        s.dfeha      = float(record[9])
        s.average_estimated_distance = float(record[10])
        s.sigd       = float(record[11])
        s.dfehab     = float(record[12])
        s.sprimtarg  = record[13]
        s.mura       = float(record[14])
        s.mudec      = float(record[15])
        s.logg       = float(record[16])
        s.snr        = float(record[17])
        s.ra         = float(record[18])
        s.dec        = float(record[19])
        s.flag       = record[20]
        s.galactic_l = float(record[21])
        s.galactic_b = float(record[22])
        s.afe        = float(record[23])
        s.dafe       = float(record[24])
        s.teff       = float(record[25])
        s.dteff      = float(record[26])
        s.photometric_parallax_distance = float(record[27])
        s.d_ferr                        = float(record[28])
        s.systematic_shift_in_distance_due_to_age      = float(record[29])
        s.systematic_shift_in_distance_due_to_binarity = float(record[30])
        s.bin_fraction      = float(record[31])
        s.plate2            = record[32]
        s.mjd2              = record[33]
        s.fiber2            = record[34]
        s.r_mag_weight_sn10 = float(record[35])
        s.type_weight_sn10  = float(record[36])
        s.r_mag_weight_sn15 = float(record[37])
        s.type_weight_sn15  = float(record[38])
        s.r_mag_weight_sn20 = float(record[39])
        s.type_weight_sn20  = float(record[40])
        s.r_mag_weight_sn25 = float(record[41])
        s.type_weight_sn25  = float(record[42])
        s.r_mag_weight_sn30 = float(record[43])
        s.type_weight_sn30  = float(record[44])
        s.r_mag_weight_sn30_alpha = float(record[45])
        s.type_weight_sn30_alpha  = float(record[46])
        s.deredened_g_minus_r     = float(record[47])
        s.original_estimated_distance = float(record[48])
        s.galactic_cartesian_x        = float(record[49])
        s.galactic_cartesian_y        = float(record[50])
        s.galactic_cartesian_z        = float(record[51])
        s.good_pm                     = record[52]

        # some conversion
        s.ra_deg  = s.ra
        s.dec_deg = s.dec
        s.ra_rad  = math.radians(s.ra)
        s.dec_rad = math.radians(s.dec)

        s.distance = s.average_estimated_distance

        x, y, z = seg.eq2cart(s.ra_rad, s.dec_rad, s.distance)
        s.cartesian_x, s.cartesian_y, s.cartesian_z = x, y, z

        s.galactic_l_rad, s.galactic_b_rad = seg.eq2gal(s.ra_rad, s.dec_rad)
        s.galactic_l_deg = math.degrees(s.galactic_l_rad)
        s.galactic_b_deg = math.degrees(s.galactic_b_rad)
        s.galactic_Z, s.galactic_R = seg.gal2ZR(s.galactic_l_rad, s.galactic_b_rad, s.distance)

        star_list.append(s)

    in_file.close()

    # Select only G stars
    gstar_list = []
    for s in star_list:
        if (s.average_estimated_distance > 0.0
            and (s.g0 - s.r0) > 0.48
            and (s.g0 - s.r0) < 0.55
            and s.r0 > 15.0
            and s.r0 < 19.0):

            gstar_list.append(s)

    output_filename = cleaned_dir + 'gstar_sample.dat'
    output_file = open(output_filename, 'wb')

    pickle.dump(gstar_list, output_file)
    sys.stderr.write('Pickle output to file {} .\n'.format(output_filename))

    output_file.close()


if __name__ == '__main__':
    main()


