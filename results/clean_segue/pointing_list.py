#!/usr/bin/env python


#----------------------
# segue plates are seleted using following SQL query:
#
# select
#   plateID, plate, tile, mjd, ra, dec, survey, programName, plateQuality, nStar
# from
#   PlateX
# where
#   PlateX.survey like "segue%"
#
#------------------------

import mw_utilities_python as mwu
import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string, csv

#------------------------------------------------------------------------------
def plate_csv(filename):
    """
    Read plates' information from csv file obtained from database using SQL.
    Return a list of plates' information. Each element in the list is a python
    dictionary of plate's information. Dictionary keys are from the header of
    the csv file, so it's the same as in the sdss database.

    For example, a plate's plateID can be called as plate[5]['plateID']
    """

    f = open(filename,'r')
    plates = []

    try:
        plist = csv.DictReader(f)
        for record in plist:
            plates.append(record)

    finally:
        f.close()

    return plates
#------------------------------------------------------------------------------
def main():

    # Get paths
    rawdata_dir = mwu.get_path.get_rawdata_path()
    cleaned_dir = mwu.get_path.get_cleandata_path()

    plates = plate_csv(rawdata_dir + 'segue.plates.csv')

    plt = []
    flag = 0
    # picking plates as needed
    for i in plates:
        if ((i['survey'] == 'segue1' or i['survey'] == 'segue2')
            and (i['programName'] == 'segue'
                 or i['programName'] == 'seguefaint'
                 or i['programName'] == 'segue2')
            and (i['plateQuality'] == 'good')
            ):
            plt.append([i['ra'], i['dec'], i['plate'], flag])

    # ignore duplicate plate id, because some plate may have more
    # than one time tag thus have duplicates in the Plates table
    for i in range(len(plt)):
        for j in range(i + 1, len(plt)):
            if plt[j][2] == plt[i][2]:
                plt[j][3] = 1  # set a flag

    # Calculate the Cartesian coordinates of centers
    for i in range(len(plt)):

        ra = math.radians(float(plt[i][0]))
        dec = math.radians(float(plt[i][1]))
        r = 1.0
        cart = seg.eq2cart(ra, dec, r);
        plt[i].insert(2, str(cart[0]));
        plt[i].insert(3, str(cart[1]));
        plt[i].insert(4, str(cart[2]));

    # combine duplicates
    for i in range(len(plt)):
        if plt[i][6] == 1:
            continue
        for j in range(i + 1, len(plt)):
            if plt[i][0] == plt[j][0] and plt[i][1] == plt[j][1]:
                plt[i].append(plt[j][5])
                plt[j][6] = 1


    # output
    fout = open(cleaned_dir + 'pointing_list.txt', 'w')
    fout.write('# reduced plate pointings\' coordinates\n')
    fout.write('# pointingID ra dec x y z plate [plate]\n')

    n = 0
    for i in plt:
        if i[6] != 1:
            i.remove(0)
            i.insert(0, str(n)) # Add a pointing ID
            n += 1
            # fout.write(string.join([x for x in i]) + "\n")
            fout.write(' '.join([x for x in i]) + '\n')

    fout.close


    # output a list of plates vs pointing ID
    plt2ptg=[]
    for i in plt:
        if i[6] != 1:
            for j in range(len(i)-6):
                plt2ptg.append([i[j+6], i[0]])

    fout = open(cleaned_dir + 'plate2pointing.dat', 'w')
    fout.write('# plate pointing\n')

    for i in plt2ptg:
        # fout.write(string.join([x for x in i]) + "\n")
        fout.write(' '.join([x for x in i]) + '\n')
    fout.close


    # read the txt pointing_list file and pickle it
    pointing_list = []
    file = open(cleaned_dir + 'pointing_list.txt', 'r')
    for line in file:
        if line.lstrip().startswith('#'):
            continue
        record = line.split()

        p = seg.Pointing() # create a pointing instance

        p.ID = record[0]
        p.ra_deg = float(record[1])
        p.dec_deg = float(record[2])
        p.ra_rad = math.radians(p.ra_deg)
        p.dec_rad = math.radians(p.dec_deg)
        p.cartesian_x = float(record[3])
        p.cartesian_y = float(record[4])
        p.cartesian_z = float(record[5])

        p.galactic_l_rad, p.galactic_b_rad = seg.eq2gal(p.ra_rad, p.dec_rad)
        p.galactic_l_deg = math.degrees(p.galactic_l_rad)
        p.galactic_b_deg = math.degrees(p.galactic_b_rad)

        p.plate = []
        for i in range(len(record) - 6):
            p.plate.append(record[6 + i])

        pointing_list.append(p)

    file.close()

    output_filename = cleaned_dir + 'pointing_list.dat'
    output_file = open(output_filename, 'wb')
    pickle.dump(pointing_list, output_file)
    output_file.close()
    sys.stderr.write('Pickle dump pointing list to {} .\n'
                     .format(output_filename))


if __name__ == '__main__' :
    main()





