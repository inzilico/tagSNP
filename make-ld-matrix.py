"""
Make LD matrix from *.hap.ld file with r2 mesures created by vcftools.
All SNPs of the region are assumed at the same chromosome.
The output files: *.map (genomic coordinates of SNPs), *.ld (LD matrix as text table), 
and *.ld.h5 (LD matrix under HDF5).
Author: Gennady Khvorykh, info@inzilico.com
Created June 19, 2024
"""

import sys
import pandas as pd
import numpy as np
import functions
import networkx as nx
import time

# Get command line arguments
input_prefix = sys.argv[1]

# Initiate variables
input_file = input_prefix + ".hap.ld"
vcf_file = input_prefix + ".vcf"
ts = time.time()

# Check input
functions.check_files([input_file, vcf_file])

# Load r2 values
d1 = pd.read_csv(input_file, sep="\t", usecols=["CHR", "POS1", "POS2", "R^2"])

# Convert edgelist to adjacency matrix
G = nx.from_pandas_edgelist(
    d1,
    source="POS1",
    target="POS2",
    edge_attr="R^2"
)

print(G)

ld = pd.DataFrame(
    nx.adjacency_matrix(G, weight="R^2").todense(),
    dtype=float
)

# Overwrite the values on the diagonal
np.fill_diagonal(ld.values, 1.0)

# Save ld matrix
ld.to_csv(input_prefix + ".ld", index=None, header=False, sep=" ")

# Save as h5py 
ld.to_hdf(input_prefix + ".ld.h5", key = 'r2', mode = 'w')

# Get genomic coordinates and rs from vcf file and save in *.map file
f1 = open(vcf_file, "r")
f2 = open(input_prefix + ".map", "w") 
for line in f1:
    if line.startswith("#"): continue
    arr = line.strip().split("\t")
    print(arr[0], arr[1], arr[2], arr[3], arr[4], file=f2)
f1.close()
f2.close()

functions.time_elepsed(ts)