#! /usr/bin/env python3

'''
    Description : 

        This script takes a two column csv file where first column corresponds to
        RESID and the second column corresonds to the respective value. This value
        can be from whatever sources, example SHAPE data. The other input file is
        the PDB file whose B-factor coulmn will be replaced by the respective
        values of second column of the csv file.

        Input arguments :  (Checkout the example given below)

            prefix          : The filename for your output PDB file (No file
                              extentsion needed)
            model           : Your input PDB file (with file extension)
            datafile        : Your comma separated CSV file (with file extension)
            selection       : LOOS selection for residues


    Usage :

       python3 csv2pdb.py prefix model datafile selection

    Example :

       python3 csv2pdb.py prefix structure.pdb datafile.csv 'resid >= 1 && resid <= 101'

    Author :

     Ashlin James Poruthoor

'''

# Import modules
import sys
import argparse
import loos
import loos.pyloos
import numpy as np

# Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('prefix', help='Handle for output files.')
parser.add_argument('model', help='Structure to be used')
parser.add_argument('datafile', help='Profile file')
parser.add_argument('selection', help='Atom selection')
args = parser.parse_args()

# System setup
model = loos.createSystem(args.model)
selection = loos.selectAtoms(model,args.selection)
residues = selection.splitByResidue()


# Read in data file
with open(args.datafile, 'r', encoding='utf-8-sig') as datafile:
    data = np.genfromtxt(datafile, delimiter=',',dtype=float)

RESID = data[:,0]
VALUE = data[:,1]

if RESID.shape[0] != VALUE.shape[0]:
    print ("Column 1 and 2 have different size. Format it accordingly")
    exit()

print("\nData file detected :\n")
print("File Name :  %s \n" % (str(args.datafile)))
print("No. of Rows : %d \n" % (RESID.shape[0]))
print("Processing PDB file : %s\n" %(str(args.model)))

if RESID.shape[0] != len(residues):
    print ("\nWARNING !!\n")
    print ("CSV file has %d rows but selection consists of only %d residues.\n" % (RESID.shape[0], len(residues)))
    print("If this is something you expected, ignore this message. Else, format your selection or CSV accordingly\n")
    print ("Checkout for missing residues that will be printed below\n")
    #  exit()

pdbFile = loos.PDB.fromAtomicGroup(selection)
outFile = open(args.prefix + ".pdb", "w")

# Get the observable value for each residue for this time point
for idx, resid in enumerate(RESID):

    Missing = True

    # Fill-in the B-factor of each atom in that residue
    for k in residues:

        if k[0].resid() == resid:
            for atom in k:
                atom.bfactor(VALUE[idx])

            Missing = False

            break

    if Missing:
        print ("WARNING! Missing residue %d \n" % (resid))


# Write out the PDB
outFile.write(str(pdbFile))
outFile.close() 
