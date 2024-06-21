"""
Subset a submatrix from LD matrix and count mean, median, rho, and logarithm of its determinant.
The SNPs in submatrix are not necessarily consequitive.
The index file has the list of SNPs for each block.
Author: Gennady Khvorykh, info@inzilico.com
Created: October 19, 2023
"""

import os
import sys
import h5py
import time
import numpy as np
import argparse

def subset_matrix(m, indexes):
    ind = [x - 1 for x in indexes]
    sm = [x[ind] for x in m[ind]]
    return(np.asmatrix(sm))

# Get arguments from command line 
parser = argparse.ArgumentParser(description="Count the features of LD submatrices")
parser.add_argument("-l", "--ld", help="/path/to/ld-matrix.h5", required=True)
parser.add_argument("-i", "--ind", help="/path/to/index.txt with two columns: \
                    block ID, commaseperated list of SNPs in the block", required=True)
parser.add_argument("-o", "--out", help="/path/to/output.txt to save output", 
                    required=True)
parser.add_argument("--r2", type=float, help="The cutoff value of r2 to estimate rho (default: 0.8)", 
                    default=0.8)
args = parser.parse_args()

# Initiate variables
h5_file = args.ld
ind_file = args.ind
output_file = args.out
r2 = args.r2
t1 = time.time()

# Check input
for file in [h5_file, ind_file]:
    if not os.path.isfile(file):
        print(file, "doesn't exist")
        sys.exit(1)

# Show input
print("LD matrix:", h5_file)
print("Index file:", ind_file)
print("Output file:", output_file)
print("r2:", r2)

# Open h5 file
h = h5py.File(h5_file, "r")
ds = h["r2"]
m = ds["block0_values"]

# Open output files
f1 = open(output_file, "w")
print("cl mean median rho logdet", file=f1)

# Loop over over file with group indexes
with open(ind_file, "r") as file:
    lines = file.readlines()
    for line in lines:
        cl, csv = line.split()
        if cl == "None": continue
        indexes = [int(i) for i in csv.split(",")]
        # Subset a matrix
        sm = subset_matrix(m, indexes)
        # Get above diagonal elements
        tr = sm[np.triu_indices(sm.shape[0], k=1)]
        v = [i.tolist() for i in np.nditer(tr.T)]
        # Count features
        rho = sum(1 for i in v if i >= r2) / len(v)
        sign, logdet = np.linalg.slogdet(sm)
        # Output
        print(cl, np.mean(v), np.median(v), rho, logdet, file=f1)

# Close files
h.close()
f1.close()

# Show the number of lines processed
print("Blocks: ", len(lines))

# Show time elapsed
dur = time.time() - t1
dur = time.strftime("%H:%M:%S", time.gmtime(dur))
print("Time spent: ", dur)
