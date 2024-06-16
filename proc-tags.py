"""
Process TAGS created by Tagger under Haploview software
Author: Gennady Khvorykh, info@inzilico.com
Creted: June 15, 2024
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

# Get command line arguments
input_file = sys.argv[1]
output_prefix = sys.argv[2]

def parse_tags_file(x: str):
    array = []
    with open(x, "r") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(("#", "Allele")): continue
            if line.startswith("Test"): break
            items = line.split("\t")
            if len(items) == 1 : continue
            array.append(items)
    df = pd.DataFrame(array)        
    return(df)

# Parser TAGS file created by Haploview 
d1 = parse_tags_file(input_file)

# Convert string to numeric
d1 = d1.astype({2: float})

# Initiate empty data frame
out = pd.DataFrame(columns = ["size", "mean"])

# Get counts and mean of r2
out["size"] = d1.groupby(1).size()
out["mean"] = d1.groupby(1)[2].mean()

# Save 
out.to_csv(output_prefix + ".tab", sep = "\t", index_label="snp")

# Save quantiles
with open(output_prefix + ".q", "w") as f:
    print(out.quantile(q=[0.25, 0.5, 0.75], axis=0), file=f) 

# Initiate plot array
fig, (ax1, ax2) = plt.subplots(1, 2)

# Add boxplot of sizes
ax1.boxplot(out["size"])

# Add boxplot of mean values
ax2.boxplot(out["mean"])

# Save 
plt.savefig(output_prefix + ".png")
