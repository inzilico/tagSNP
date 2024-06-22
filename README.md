# Identification of tagSNP 

## Description

The repo contains scripts to automate the identification of tagging single nucleotide polymorphisms (tagSNP) with [Haploview 4.2](https://www.broadinstitute.org/haploview/haploview), [Clustag v2](https://www.engineeringletters.com/editors/SIAO/CLUSTAG/CLUSTAG.htm), and [gpart R package 1.2.0](https://bioconductor.riken.jp/packages/3.9/bioc/html/gpart.html). The scripts were tested under Ubuntu 22.04.4 LTS. We assume the paths to the softwares applied in the scripts and other resources are in the `res.cfg` file located at the folder with the scripts. Each row of the file has the software name and the path to the software seperated by comma. Please, use the links to the software websites to find out how to install them.

## Subset SNPs 

* **subset.pl** subsets SNPs from CEU population of [1000 Genomes project](https://www.internationalgenome.org) by genomic coordinates and MAF.
* **subset-from-plink.pl** subsets SNPs from [Plink 1.9](https://www.cog-genomics.org/plink) binary files by genomic coordinates and MAF.

## tagSNP identification 

### Haploview 4.2

[Haploview 4.2](https://www.broadinstitute.org/haploview/haploview) runs haplotype analysis. It also implements Paul de Bakker's [Tagger](https://software.broadinstitute.org/mpg/tagger/) tagSNP selection algorithm. The [command line options](https://www.broadinstitute.org/haploview/chapter-3-command-line-options) of the tool allow to apply it in scripts. 

* **vcf2haploview.R** converts vcf files into input files for Haploview.
* **run-tagger.py** a wrapper script to find out tagSNP with Tagger algorithm from Haploview. 
* **proc-tags.py** post-process TAGS created by Haploview.
* **proc-haploview-tags-01.py** defines the indexes of SNPs tagged by tagSNPs given in ped.TAGS file created by Haploview. 

### Clustag 2

[Clustag v2](https://www.engineeringletters.com/editors/SIAO/CLUSTAG/CLUSTAG.htm) is a software that applies hierarchical clustering and graph methods for selecting tagSNPs. It is emplemented in Java.

* **2clustag.R** creates input files for Clustag from vcf-file. [bcftools](https://samtools.github.io/bcftools) should be in `$PATH` global variable. 
* **clustag.sh** is a wrapper script for running Clustag. It should be lanched from the same folder as input data.
* **proc-clustag-01.py** post-process `*.members.txt` file created by Clustag software. Get sizes of clusters. 
* **proc-clustag-02.py** post-process `*.out` file created with Clustag. Get the distribution of cluster sizes and mean values of r2 between tagSNP and other SNPs in a cluster.
* **proc-clustag-03.py** defines the indexes of tagged SNPs given in `*.out` file. 
 
### gpart R package 1.2.0

[gpart R package](https://bioconductor.riken.jp/packages/3.9/bioc/html/gpart.html) is the implementation of BIG-LD method ([Kim et al., 2018](https://academic.oup.com/bioinformatics/article/34/3/388/4282661)), a block partition method based on interval graph modeling of LD bins which are clusters of strong pairwise LD SNPs, not necessarily physically consecutive.

* **vcf2gpart.R** converts vcf into geno/info files for gpart. The R package [VariantAnnotation](https://www.bioconductor.org/packages/release/bioc/html/VariantAnnotation.html) to process vcf file is required.

```bash
vcf2gpart.R path/to/mydata.vcf path/to/output_folder
```

## Other scripts and files

* **count-submatrix-features.py** counts mean, median, rho and determinant of LD submatrices composed of consequitive SNPs.
* **count-mosaic-submatrix-features.py** counts mean, median, rho and determinant of LD submatrices composed on SNPs not necessarily consequitive.   
* **functions.py** contains functions to assist data processing with scripts in Python 3.8.
* **make-ld-matrix.py** creats LD matrix under text and HD5F formats from hap.ld file with r2 values obtained with [vcftools](https://vcftools.github.io/index.html). 

```bash
python3 make-ld-matrix.py path/to/prefix

``` 
`prefix` corresponds to prefix.hap.ld and prefix.vcf files. 

The files prefix.ld, prefix.ld.h5 and prefix.map will be created at the same folder as imput file. prefix.map contains the list of rs IDs with genomic coordinates extracted from prefix.vcf file. 

* **plot-hist.R** plot the histogram of MAF (minor allele frequencies) counted with [Plink 1.9](https://www.cog-genomics.org/plink/) --freq argument.

## Use cases

The scripts in this repo were applied in the following researches:

Khvorykh, G., Khrunin, A., Filippenkov, I., Stavchansky, V., Dergunova, L., Limborska, S. A Workflow for Selection of Single Nucleotide Polymorphic Markers for Studying of Genetics of Ischemic Stroke Outcomes. Genes 2021, 12, 328. https://doi.org/10.3390/genes12030328 

