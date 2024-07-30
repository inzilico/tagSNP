"""
Estimate tagSNP with Tagger solution implemented in Haploview 4.2 software.
The pairwise tagging algorithm is applied. 
The Gabriel blocks are also estimated and LD heatmap is created. 
Author: Gennady Khvorykh, info@inzilico.com
Created: June 14, 2024
"""

import functions
import sys
import os
from subprocess import run

# Get command line arguments
if len(sys.argv) < 2:
    print("Missing path/to/prefix")
    sys.exit(1)
input_prefix = sys.argv[1]

# Initiate variables
ped_file = input_prefix + ".ped"
info_file = input_prefix + ".info"
script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
res_file = os.path.join(script_path, "res.cfg")

# Check input
functions.check_files([ped_file, info_file, res_file])

# Show input
print("\nInput:", input_prefix)

# Load reasources
res = functions.load_resources(res_file)

# Apply Tagger
cmd = f'{res["java"]} -jar {res["haploview"]} \
    -nogui \
    -pedfile {ped_file} \
    -info {info_file} \
    -blockoutput GAB \
    -compressedpng \
    -ldcolorscheme RSQ \
    -pairwiseTagging'
run(cmd, shell=True, check=True)

