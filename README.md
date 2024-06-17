# Description

The repo contains the scripts to automate the identification of tagging single nucleotide polymorphisms (tagSNP) with different approaches and softwares.

# Scripts

We assume that the paths to the softwares applied in the scripts below are in the `res.cfg` file located at the folder with the script. Each row of the file has the software name and the path to the software seperated by comma. 

* **2clustag.R** creates input files for CLUSTAG tool from vcf. bcftools should be in $PATH. 
* **clustag.sh** automate the tagSNP identification with Clustag software. 
* **functions.py** contains functions to assist data processing 
* **plot-hist.R** plot the histogram of MAF (minor allele frequencies) counted with Plink --freq argument
* **proc-tags.py** post-process TAGS created by Haploview 4.2
* **run-tagger.py** a wrapper script to find out tagSNP with Tagger algorithm from Haploview 4.2 sogtware
* **subset.pl** subsets SNPs from CEU population of 1000 Genomes project by genomic coordinates and MAF
* **subset-from-plink.pl** subset SNPs from Plink binary file by genomic coordinates and MAF
* **vcf2haploview.R** converts vcf files into haps for haploview
* **vcf2gpart.R** convert vcf to input files of gpart R package  

# Softwares

* **Clustag** is hierarchical clustering and graph methods for selecting tagSNPs. It is emplemented in Java. [website](https://www.engineeringletters.com/editors/SIAO/CLUSTAG/CLUSTAG.htm).