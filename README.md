# Identification of tagging single nucleotide polymorphisms 

## Description

The repo contains scripts to automate the identification of tagging single nucleotide polymorphisms (tagSNP) with [Haploview 4.2](https://www.broadinstitute.org/haploview/haploview), [Clustag v2](https://www.engineeringletters.com/editors/SIAO/CLUSTAG/CLUSTAG.htm), [gpart R package 1.2.0](https://bioconductor.riken.jp/packages/3.9/bioc/html/gpart.html), and [Tagster 1.0](https://www.niehs.nih.gov/research/resources/software/epidemiology/tagster). The scripts were tested under Ubuntu 22.04.4 LTS. We assume the paths to the softwares applied in the scripts and other resources are in the `res.cfg` file located at the folder with the scripts. Each row of the file has the software name and the path to the software seperated by comma. Please, use the links to the software websites to find out how to install them.

## Subset SNPs 

* **subset.pl** subsets SNPs from vcf file, e.g., downloaded from [1000 Genomes project](https://www.internationalgenome.org), by genomic coordinates and MAF.
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
 
### Tagster 1.0

[Xu at el., 2007](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2782964/)

[Download Tagster](https://www.niehs.nih.gov/research/resources/software/epidemiology/tagster)

* **vcf2tagster.py** converts vcf file with phased genotypes into input file for Tagster software.

```bash
python3 vcf2tagster.py -i path/to/filename.vcf -o path/to/filename -g gene_name
```

### FESTA 2.0

[Download](https://github.com/emorybiostat/FESTA/tree/master/FESTA/download/Ver2.0)

[Qin et al., 2006](https://pubmed.ncbi.nlm.nih.gov/16269414/)


## Other scripts and files

* **count-centrality.py** counts Bonacich centrality for weighted undirected graps formed by SNPs in blocks.
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

* **vcf2haplotypes.py** outputs haplotypes from phased vcf file. The minor allele is coded as 1 and the major as 0.

```bash
python3 vcf2haplotypes.py -i path/to/filename.vcf -o path/to/filename
```



## Other softwares

### gpart R package 1.2.0

[gpart R package](https://bioconductor.riken.jp/packages/3.9/bioc/html/gpart.html) is the implementation of BIG-LD method ([Kim et al., 2018](https://academic.oup.com/bioinformatics/article/34/3/388/4282661)), a block partition method based on interval graph modeling of LD bins which are clusters of strong pairwise LD SNPs, not necessarily physically consecutive.

* **vcf2gpart.R** converts vcf into geno/info files for gpart. The R package [VariantAnnotation](https://www.bioconductor.org/packages/release/bioc/html/VariantAnnotation.html) to process vcf file is required.

```bash
vcf2gpart.R path/to/mydata.vcf path/to/output_folder
```
* **run-gpart.R** is a wrapper script to apply BIG-LD with gpart.  

```bash
Rscript run-gpart.R <input>
```
input: path/to/prefix of prefix.{info,geno} files

## Use cases

The scripts in this repo were applied in the following researches:

Khrunin, A.V.; Khvorykh, G.V.; Arapova, A.S.; Kulinskaya, A.E.; Koltsova, E.A.; Petrova, E.A.; Kimelfeld, E.I.; Limborska, S.A. The Study of the Association of Polymorphisms in LSP1, GPNMB, PDPN, TAGLN, TSPO, and TUBB6 Genes with the Risk and Outcome of Ischemic Stroke in the Russian Population. Int. J. Mol. Sci. 2023, 24, 6831. https://doi.org/10.3390/ijms24076831.

Khrunin, A.V.; Khvorykh, G.V.; Rozhkova, A.V.; Koltsova, E.A.; Petrova, E.A.; Kimelfeld, E.I.; Limborska, S.A. Examination of Genetic Variants Revealed from a Rat Model of Brain Ischemia in Patients with Ischemic Stroke: A Pilot Study. Genes 2021, 12, 1938. https://doi.org/10.3390/genes12121938.

Khvorykh, G., Khrunin, A., Filippenkov, I., Stavchansky, V., Dergunova, L., Limborska, S. A Workflow for Selection of Single Nucleotide Polymorphic Markers for Studying of Genetics of Ischemic Stroke Outcomes. Genes 2021, 12, 328. https://doi.org/10.3390/genes12030328 

Khrunin A.V., Khvorykh G.V., Gnatko E.D., Filippenkov I.B., Stavchansky V.V., Dergunova L.V., Limborska S.A. Study of polymorphism of human genes, orthologues of which are functionally involved in the response to experimental brain ischemia in model systems. Medical Genetics. 2020;19(5):83-85. (In Russ.) https://doi.org/10.25557/2073-7998.2020.05.83-85.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12801392.svg)](https://doi.org/10.5281/zenodo.12801392)
