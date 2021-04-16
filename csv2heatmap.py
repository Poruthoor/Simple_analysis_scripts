#! /usr/bin/env python3

'''
    Description : 

        This script takes 2 csv files as input and create heatmaps for each and
        create a difference heatmap. 

        It is assumed that each csv files are formatted for the 2D surface plot.
        That is, the rows and coulmns coresponds to what you need to see in plot.
        More about this in PITFALLS.

        This script does not do any preprocessing other than making the shape of
        both csv files equal with additional rows/columns filled with ZEROS.
        This makes the difference plot meaningful.

        NOTE :

            The difference is taken as follows:
                difference = datafile_1 - datafile_2

        Thus, imput your csv files accordingly

        PITFALLS:

        One gottcha with using imshow() is that your csv file determines
        where your origin of the plot lies. Here it is assumed that (1,1) point
        in the plot is at the top left of the plot and the respective data comes
        from row = 1, col =1. If this is not the case for you, you might need to
        tweak this code a bit

        Input arguments :  (Checkout the example given below)

            prefix          : The filename for your output PDB file (No file
                              extentsion needed)
            datafile_1      : Your SPACE separated CSV file (with file extension)
            datafile_2      : Your SPACE separated CSV file (with file extension)
            shiftByOne      : If your csv is 0 indexed and your PDB is one
                              indexed, you might need to turn this on.
                              (default = True)


    Usage :

       python3 csv2heatmap.py prefix datafile_1 datafile_2 shiftByOne=True

    Example :

       python3 csv2heatmap.py heatmap 4Y1M.csv 4Y1J.csv shiftByOne=True

    Author :

     Ashlin James Poruthoor

'''

# Import modules
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('prefix', help='Handle for output files.')
parser.add_argument('datafile_1', help='csv file 1')
parser.add_argument('datafile_2', help='csv file 2')
parser.add_argument('--shift', dest='shiftByOne', default=True, help='shift by one (default:True)')
args = parser.parse_args()

# Read in data file
with open(args.datafile_1, 'r', encoding='utf-8-sig') as datafile_1:
    data_1 = np.loadtxt(datafile_1, delimiter=' ',dtype=float, ndmin=2)

with open(args.datafile_2, 'r', encoding='utf-8-sig') as datafile_2:
    data_2 = np.loadtxt(datafile_2, delimiter=' ',dtype=float, ndmin=2)

max_rows = max(data_1.shape[0],data_2.shape[0])
max_cols = max(data_1.shape[1],data_2.shape[1])

# Check for the dimensions
if data_1.shape[0] != data_2.shape[0]:
    print ("\nCSV file 1  has %d rows but CSV file 2 has %d rows.\n" % (data_1.shape[0], data_2.shape[0]))
    print ("Formatting it accordingly by adding zeros to the extra row(s)\n")

if data_1.shape[1] != data_2.shape[1]:
    print ("CSV file 1  has %d cols but CSV file 2 has %d cols.\n" % (data_1.shape[1], data_2.shape[1]))
    print ("Formatting it accordingly by adding zeros to the extra col(s)\n")

#Formatting the data

if args.shiftByOne :

    F_data_1 = np.zeros((max_rows+1,max_cols+1))
    F_data_2 = np.zeros((max_rows+1,max_cols+1))

    F_data_1[1:data_1.shape[0]+1,1:data_1.shape[1]+1] = data_1
    F_data_2[1:data_2.shape[0]+1,1:data_2.shape[1]+1] = data_2

else :

    F_data_1 = np.zeros((max_rows,max_cols))
    F_data_2 = np.zeros((max_rows,max_cols))

    F_data_1[:data_1.shape[0],:data_1.shape[1]] = data_1
    F_data_2[:data_2.shape[0],:data_2.shape[1]] = data_2

print ("Creating differnce matrix. NOTE : Diff = File 1 - File 2\n")
Diff_data =  F_data_1 - F_data_2

#Plotting

file_id = [str(args.datafile_1),str(args.datafile_2), "Difference"]
file_id_itr = 0

for data in (F_data_1,F_data_2,Diff_data):

    print ("Plotting %s ....\n" % (file_id[file_id_itr]))

    fig, ax0 = plt.subplots()
    divnorm = colors.TwoSlopeNorm(vcenter=0.)
    im0 = plt.imshow(data,interpolation='none', cmap='seismic', norm=divnorm)

    cbar = fig.colorbar(im0,ax=ax0)

    if args.shiftByOne:
        ax0.set_xlim(left=1)
        ax0.set_ylim(top=1)

    filename = str(args.prefix) + "_" + file_id[file_id_itr] +".png"
    file_id_itr += 1
    plt.savefig(filename)
    print ("Done")
