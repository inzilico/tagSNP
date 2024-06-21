"""
Post-process the output file (*.members.txt) created by Clustag software.
Get sizes of clusters. 
Author: Gennady Khvorykh, info@inzilico.com
Created: June 18, 2024
"""

import sys
import functions
import pandas as pd
from matplotlib import pyplot as plt
 
# Get command line arguments
input_file = sys.argv[1]
output_prefix = sys.argv[2]

# Check input
functions.check_files([input_file])

# Load input 
d1 = pd.read_csv(input_file, sep="\t")

# Initiate empty data frame
out = pd.DataFrame(columns = ["size"])

# Get sizes of clusters
out["size"] = d1.groupby("Cluster").size()
print("# of clusters:", out.shape[0])

# Save 
out.to_csv(output_prefix + ".tab", sep = "\t", index_label="cluster")

# Save quantiles
with open(output_prefix + ".q", "w") as f:
    print(out["size"].quantile(q=[0.25, 0.5, 0.75]), file=f) 

# Plot the boxplot of cluster sizes
plt.boxplot(out["size"])
plt.savefig(output_prefix + ".sizes.png")


