# Description

The repo contains the scripts to assist tagSNP selection.

# Scripts

* **2clustag.R** creates input files for CLUSTAG tool from vcf
* **subset.pl** subsets SNPs from CEU population of 1000 Genomes project by genomic coordinates and MAF
* **subset-from-plink.pl** subset SNPs from Plink binary file by genomic coordinates and MAF
* **vcf2haploview.R** converts vcf files into haps for haploview
* **vcf2gpart.R** convert vcf to input files of gpart R package  
* **plot-hist.R** plot the histogram of MAF (minor allele frequencies) counted with Plink --freq argument
* **proc-tags.py** post-process TAGS created by Haploview 4.2
* **run-tagger.py** a wrapper script to find out tagSNP with Tagger algorithm from Haploview 4.2 sogtware
* **functions.py** contains functions to assist data processing 
