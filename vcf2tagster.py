"""
Convert vcf file to input file for tagSNP selection by Tagster software (Xu at el., 2007). 
The vcf contains phased data of a genomic region from a single chromosome. 

Usage: vcf2tagster.py -i <input> -o <output> -g gene
    input: path/to/filename.vcf
    output: path/to/filename
    gene: gene id

Author: Gennady Khvorykh, info@inzilico.com
Created: July 30, 2024

Link to download Tagster: https://www.niehs.nih.gov/research/resources/software/epidemiology/tagster

Reference:
Xu Z, Kaplan NL, Taylor JA. TAGster: efficient selection of LD tag SNPs in single or multiple populations. 
Bioinformatics. 2007 Dec 1;23(23):3254-5. doi: 10.1093/bioinformatics/btm426. 
Epub 2007 Sep 7. PMID: 17827206; PMCID: PMC2782964.
"""

import os, sys
import functions
import argparse

# Initiate argument parser
parser = argparse.ArgumentParser(prog="vcf2tagster.py",
                                 description="Convert vcf file to input file for tagSNP selection by Tagster software")
parser.add_argument("-i", "--input", type=str, help="path/to/filename.vcf", required=True)
parser.add_argument("-o", "--output", type=str, help="path/to/filename to save output", required=True)
parser.add_argument("-g", "--gene", type=str, help="gene name (default=gene)", default="gene")

# Get command line arguments
args = parser.parse_args()

# Iniate variables
input_file = args.input
output_file = args.output
gene = args.gene

# Check input
functions.check_files([input_file])

# Show input
print("Input:", input_file)
print("Output:", output_file)
print("gene:", gene)

# Parser vcf file
l = functions.code_genotypes(input_file)

# Add gene and save
with open(output_file, "w") as f:
    for x in l:
        x.insert(0, gene)
        print(",".join(map(str, x)), file=f)

print("Records saved:", len(l))