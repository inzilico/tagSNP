"""
Subset submatrix from LD matrix by the list of SNPs given as indexes. 
The input are LD matrix, the file with indexes of SNPs under consideration, 
the file with genomic coordinates of SNPs, and the path with prefix to save output files. 
The file with genomic coordinates has three columns (chrom, SNP ID, and position in bp). 
Author: Gennady Khvorykh, info@inzilico.com
Created June 22, 2024.
"""

import argparse
import functions
import time
import h5py
import numpy as np
import pandas as pd

# Get command line arguments
parser = argparse.ArgumentParser(prog="subset-submatrix-01.py", 
                                 description="Subset submatrix from LD matrix by the list of SNPs given as indexes.")
parser.add_argument("-l", "--ld", 
                    help="path/to/filename.ld.h5 with LD matrix under HD5F format", required=True)
parser.add_argument("-i", "--ind", 
                    help="path/to/filename.txt with indexes of SNPs in blocks", required=True)
parser.add_argument("-m", "--map", 
                    help="path/to/filename.txt with genomic coordinates of SNPs", required=True)
parser.add_argument("-o", "--out", 
                    help="path/to/prefix to save output files", 
                    required=True)
args = parser.parse_args()

# Initiate varibles
ld_file = args.ld
ind_file = args.ind
output_prefix = args.out
map_file = args.map
ts = time.time()

# Show input
print("LD matrix:", ld_file)
print("Index file:", ind_file)
print("Map file:", map_file)
print("Output prefix:", output_prefix)

# Check input
functions.check_files([ld_file, ind_file, map_file])

# Open h5 file with LD matrix
h = h5py.File(ld_file, "r")
ds = h["r2"]
m = ds["block0_values"]

print("LD matrix shape:", m.shape[0], "x", m.shape[1])

# Load map file
map = pd.read_csv(map_file, sep=" ")
print("No of SNPs in map file:", map.shape[0])

# Loop over over file with indexes
with open(ind_file, "r") as file:
    lines = file.readlines()
    print("No of blocks:", len(lines))
    for line in lines:
        cl, csv = line.split()
        if cl == "None": continue
        indexes = [int(i) for i in csv.split(",")]
        # Subset a submatrix
        sm1 = functions.subset_matrix(m, indexes)
        # Get rs IDs
        ind = [x - 1 for x in indexes]
        rs = map.iloc[ind, 1]
        # Save a matrix to file
        np.savetxt(fname=f'{output_prefix}.{cl}.ld', 
                   X=sm1, 
                   header=' '.join([str(i) for i in rs]),
                   comments="",
                   fmt="%.7f")

#Show time elapsed
functions.time_elepsed(ts)
