"""
Post-process ped.TAGS file created by Haploview 
to define the indexes of SNPs tagged by tagSNPs.
Only the blocks with two or more tagged SNPs are considered.
Author: Gennady Khvorykh, info@inzilioc.com
Created: June 20, 2024
"""

import sys
import functions
import pandas as pd

# Get command line arguments
input_prefix = sys.argv[1]

# Initite variables
tag_file = input_prefix + ".ped.TAGS"
info_file = input_prefix + ".info"
index_file = input_prefix + ".ind"

# Check input
functions.check_files([tag_file, info_file])

# Find the line number to start to load data
n = 0
with open(tag_file, "r") as f:
    for line in f:
        if "Alleles Captured" in line: break
        n += 1

# Load tagSNPs
d1 = pd.read_csv(tag_file, sep="\t", skiprows=n)
print("No of tagSNPs:", d1.shape[0])

# Load info file
info = pd.read_csv(info_file, sep=" ", header=None, names=["rs", "pos"])
info.sort_values(by="pos", inplace=True)
info["ind"] = info.index + 1
print("No of SNPs:", info.shape[0])

# Process each row of data frame
f = open(index_file, "w")
for row in d1.itertuples(index=False):
    test = row[0]
    snps = row[1].split(",")
    if len(snps) == 1: continue
    indexes = [info.loc[info["rs"] == rs, "ind"].values[0] for rs in snps]
    indexes.sort()
    print(test, ",".join(str(i) for i in indexes), file=f)
f.close()

