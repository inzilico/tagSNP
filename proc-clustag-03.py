"""
Post-process the output file (*.out) created by Clustag software. 
Define the indexes of SNPs tagged by tagSNPs and save in *.ind file. 
Author: Gennady Khvorykh, info@inzilico.com
Created: June 21, 2024
"""

import sys
import functions
import pandas as pd

# Get command line arguments
input_prefix = sys.argv[1]
vcf_file = sys.argv[2]

# Iniate variables
input_file = input_prefix + ".out"
output_file = input_prefix + ".ind"

# Check input
functions.check_files([input_file, vcf_file])

# Find out the row to start the import
n = 0
with open(input_file, "r") as f:
        for line in f:
            if "Similarity with tagging SNP" in line: break
            n += 1
                 
# Load data
d1 = pd.read_csv(input_file, sep="\t", skiprows=n, skip_blank_lines=True)

# Correct rs 
d1["Name"] = d1["Name"].str.replace("*", "")

# Group SNPs by cluster ID
d2 = d1.groupby("Cluster")["Name"].apply(list)
print("No of tagSNP:", len(d2))

# Get genomic coordinates and rs from vcf file 
info = []
f1 = open(vcf_file, "r")
for line in f1:
    if line.startswith("#"): continue
    arr = line.strip().split("\t")
    info.append([arr[1], arr[2]])
f1.close()

# Convert array to data frame
d3 = pd.DataFrame(info, columns=["pos", "rs"])
d3.sort_values("pos", inplace=True)
d3["ind"] = d3.index + 1
print("No of SNPs:", d3.shape[0])

# Get indexes and save in the file
f = open(output_file, "w")
for test, snps in d2.items():
    if len(snps) == 1: continue
    indexes = [d3.loc[d3["rs"] == rs, "ind"].values[0] for rs in snps]
    indexes.sort()
    print(test, ",".join(str(i) for i in indexes), file=f)
f.close()