"""
Subset a submatrix from LD matrix and count its features.
The SNPs in block are assumed to be consequitive.
The index file has the index of the first and the last SNP in the block.
Author: Gennady Khvorykh, info@inzilico.com
Created: October 18, 2023
"""

import os
import sys
import h5py
import time
import numpy as np
import argparse

# Get command line arguments
parser = argparse.ArgumentParser(description="Count the features of submatrices")
parser.add_argument("-l", "--ld", help="/path/to/ld-matrix.h5", required=True)
parser.add_argument("-i", "--ind", 
                    help="/path/to/index.txt with three columns: \
                    block ID, firt and last index of SNP in the block", 
                    required=True)
parser.add_argument(
    "-o", "--out", help="/path/to/output.txt to save output", required=True
)
parser.add_argument("--r2", type=float, help="The cutoff value of r2 (default: 0.8)", default=0.8)
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
print("cl i1 i2 mean median rho logdet", file=f1)

# Loop over over file with group indexes
with open(ind_file, "r") as file:
    lines = file.readlines()
    for line in lines:
        cl, i1, i2 = line.split()
        i1 = int(i1) - 1
        i2 = int(i2)
        # Subset a matrix
        sm = m[i1:i2, i1:i2]
        # Get above diagonal elements
        v = sm[np.triu_indices(sm.shape[0], k=1)]
        # Count features
        rho = sum(1 for i in v if i >= r2) / len(v)
        sign, logdet = np.linalg.slogdet(sm)
        # Output
        print(cl, i1 + 1, i2, np.mean(v), np.median(v), rho, logdet, file=f1)

# Close files
h.close()
f1.close()

# Show the number of lines processed
print("Blocks: ", len(lines))

# Show time elapsed
dur = time.time() - t1
dur = time.strftime("%H:%M:%S", time.gmtime(dur))
print("Time spent: ", dur)
