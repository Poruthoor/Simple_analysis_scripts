# Simple_analysis_scripts
__________________________

These are scripts that were generated to do simple analysis. It is mainly created for labs outside Grossfield Lab at the University of Rochester that take advantage of [LOOS](https://github.com/GrossfieldLab/loos) package. 

To install the LOOS package, refer [here](https://github.com/GrossfieldLab/loos/blob/main/INSTALL.md).

Some scripts require LOOS to implement, and some do not. Scripts that require LOOS package are labeled with 🌟

## Contents

1. `csv2pdb.py` : Replaces the B-factor column in input .pdb with custom value in your .csv file. 🌟  
2. `csv2heatmap.py`: Creates difference heatmap from two input .csv files

### 1. csv2pdb.py 🌟

```
    Description :

        This script takes a two-column .csv file where the first column corresponds to
        RESID and the second column corresponds to the respective value. This value
        can be from whatever sources, for example, SHAPE data. The other input file is
        the PDB file, whose B-factor column will be replaced by the respective values
        of the second column of the .csv file.

        Input arguments :  (Check out the example given below)

            prefix          : The filename for your output PDB file (No file
                              extentsion needed)
            model           : Your input PDB file (with file extension)
            datafile        : Your comma separated CSV file (with file extension)
            selection       : LOOS selection for residues


    Usage :

       python3 csv2pdb.py prefix model datafile selection

    Example :

       python3 csv2pdb.py prefix structure.pdb datafile.csv 'resid >= 1 && resid <= 101'

```

### 2. csv2heatmap.py

```
Description :

        This script takes two .csv files as input and creates heatmaps for each and
        create a difference heatmap.

        It is assumed that each .csv file is formatted for the 2D surface plot.
        That is, the rows and columns correspond to what you need to see in the plot.
        More about this in PITFALLS.

        This script does not do any preprocessing other than making the shape of
        both .csv files equal with additional rows/columns filled with ZEROS.
        This makes the difference plot meaningful.

        NOTE :

            The difference is taken as follows:
                difference = datafile_1 - datafile_2

        Thus, input your .csv files accordingly.

        PITFALLS:

        One gotcha using imshow() is that your .csv file determines where your plot's
        origin lies. Here it is assumed that (1,1) point in the plot is at the top
        left of the plot and the respective data comes from row = 1, col =1. If this
        is not the case for you, you might need to tweak this code a bit

        Input arguments :  (Check out the example given below)

            prefix          : The filename for your output PDB file (No file
                              extentsion needed)
            datafile_1      : Your SPACE separated CSV file (with file extension)
            datafile_2      : Your SPACE separated CSV file (with file extension)
            --shift         : [OPTIONAL] correction to make python array and PDB
                               are one indexed, you might not need to turn this
                               off. (default = True)


    Usage :

       python3 csv2heatmap.py prefix datafile_1 datafile_2 --shift=[BOOL,default=True]

    Example :

       python3 csv2heatmap.py heatmap 4Y1M.csv 4Y1J.csv --shift=True
```
