# Identification of tagSNP 

## Description

The repo contains scripts to automate the identification of tagging single nucleotide polymorphisms (tagSNP) with different approaches and softwares.
The scripts were tested under Ubuntu 22.04.4 LTS. We assume the paths to the softwares applied in the scripts are in the `res.cfg` file located at the folder with the script. Each row of the file has the software name and the path to the software seperated by comma. Please, use the links to the software websites to find out how to install them.

## Subset SNPs 

* **subset.pl** subsets SNPs from CEU population of [1000 Genomes project](https://www.internationalgenome.org) by genomic coordinates and MAF.
* **subset-from-plink.pl** subset SNPs from [Plink 1.9](https://www.cog-genomics.org/plink) binary files by genomic coordinates and MAF.

## tagSNP identification 

### Haploview 4.2

[Haploview 4.2](https://www.broadinstitute.org/haploview/haploview) runs haplotype analysis. It also implements Paul de Bakker's [Tagger](https://software.broadinstitute.org/mpg/tagger/) tagSNP selection algorithm. The [command line options](https://www.broadinstitute.org/haploview/chapter-3-command-line-options) of the tool allow to apply it in scripts. 

* **vcf2haploview.R** converts vcf files into input files for Haploview.
* **run-tagger.py** a wrapper script to find out tagSNP with Tagger algorithm from Haploview. 
* **proc-tags.py** post-process TAGS created by Haploview.

### Clustag 2

[Clustag v2](https://www.engineeringletters.com/editors/SIAO/CLUSTAG/CLUSTAG.htm) is a software that applies hierarchical clustering and graph methods for selecting tagSNPs. It is emplemented in Java.

* **2clustag.R** creates input files for Clustag from vcf-file. [bcftools]() should be in $PATH global variable. 
* **clustag.sh** is a wrapper script for running Clustag. It should be lanched from the same folder as input data.


### gpart R package

[gpart R package](https://github.com/sunnyeesl/BigLD?tab=readme-ov-file) is the implementation of BIG-LD approch, a block partition method based on interval graph modeling of LD bins which are clusters of strong pairwise LD SNPs, not necessarily physically consecutive.
The [article](https://academic.oup.com/bioinformatics/article/34/3/388/4282661) provides more details on the method.

* **vcf2gpart.R** convert vcf to input files for gpart  

## Other scripts and files

* **functions.py** contains functions to assist data processing with scripts in Python 3.8.
* **plot-hist.R** plot the histogram of MAF (minor allele frequencies) counted with [Plink 1.9](https://www.cog-genomics.org/plink/) --freq argument.