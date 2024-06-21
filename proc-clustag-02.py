"""
Post-process the output file (*.out) created by Clustag software.
Get the distribution of cluster sizes and mean values of r2 between tagSNP and other SNPs in cluster. 
Author: Gennady Khvorykh, info@inzilico.com
Created: June 18, 2024
"""

import sys
import functions
import pandas as pd
from matplotlib import pyplot as plt
import re 

def rows_to_import(x: str):
    """
    Find out the first and last rows to import data
    """
    n, n1, n2 = 0, 0, 0
    with open(x, "r") as f:
        for line in f:
            n = n + 1
            if re.search("Tagging SNP", line): 
                n1 = n
            if re.search("Cluster members", line):
                n2 = n
                break
    return((n1, n2))

 
# Get command line arguments
input_file = sys.argv[1]
output_prefix = sys.argv[2]

# Check input
functions.check_files([input_file])

# Find out rows to import 
n1, n2 = rows_to_import(input_file)

# Load data
d1 = pd.read_csv(input_file, sep="\t", skiprows=n1-1, nrows=n2-n1-1)
print("# of clusters:", d1.shape[0])

# Save 
d1.to_csv(output_prefix + ".tab", sep = "\t", index=False)

# Save quantiles
with open(output_prefix + ".q", "w") as f:
    print(d1[["Size", "Avg. sim."]].quantile(q=[0.25, 0.5, 0.75], axis=0), file=f) 

# Initiate plot array
fig, (ax1, ax2) = plt.subplots(1, 2)

# Add boxplot of sizes
ax1.boxplot(d1["Size"])

# Add boxplot of mean values
ax2.boxplot(d1["Avg. sim."])

# Save 
plt.savefig(output_prefix + ".png")

