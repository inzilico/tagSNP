"""
Get haplotypes from phased vcf file.  
The major allele is denoted as 0 and minor as 1. 

Usage: vcf2haplotypes.py -i <input> -o <output>
    input: path/to/filename.vcf
    output: path/to/filename

Author: Gennady Khvorykh, info@inzilico.com
Created: August 1, 2024
"""

import functions
import argparse

# Initiate argument parser
parser = argparse.ArgumentParser(prog="vcf2tagster.py",
                                 description="Convert vcf file to input file for tagSNP selection by Tagster software")
parser.add_argument("-i", "--input", type=str, help="path/to/filename.vcf", required=True)
parser.add_argument("-o", "--output", type=str, help="path/to/filename to save output", required=True)

# Get command line arguments
args = parser.parse_args()

# Iniate variables
input_file = args.input
output_file = args.output

# Check input
functions.check_files([input_file])

# Show input
print("Input:", input_file)
print("Output:", output_file)

# Get haplotypes 
haplotypes = functions.get_haplotypes(input_file)

# Save
haplotypes.to_csv(output_file, index=False, header=False)

print("Haplotyes saved:", haplotypes.shape[0])