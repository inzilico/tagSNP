#!/usr/bin/Rscript
## Convert vcf files for for gpart R package 
## Usage: vcf2gpart <input> <output>
##        input: path/to/mydata.vcf
##        output: path/to/folder to save the output

suppressPackageStartupMessages(require(dplyr)) 
args <- commandArgs(TRUE)

# TODO: comment after debugg
# args[1] <- "~/data/ortho/maf10/CPLX2.vcf"
# args[2] <- "~/data/ortho/maf10/gp/CPLX2"

# Check arguments provided
if(length(args) < 2) stop("Missing arguments...", call. = F)

# Initilize
vcff <- args[1]
id <- basename(vcff) %>% sub(pattern = ".vcf", replacement = "")
output <- args[2]

# Check file exists
if(!file.exists(vcff)) stop(vcff, " isn't found", call. = F)

message("Sample: ", id)

# Create folder for output if not exist
if(!dir.exists(output)) dir.create(output, recursive = T)

# Load vcf 
vcf <- VariantAnnotation::readVcf(vcff) 

# Create SNPinfo data and save as *.info file
gr <- vcf %>% SummarizedExperiment::rowRanges()
snpinfo <- data.frame(chrN = GenomicRanges::seqnames(gr) %>% as.integer(),
                      rsID = names(gr),
                      bp = GenomicRanges::start(gr))
data.table::fwrite(snpinfo, sprintf("%s/%s.info", output, id), 
                   col.names = T, sep = " ", verbose = F)

# Get genotypes
g <- VariantAnnotation::geno(vcf)[["GT"]]

# Get ref and alt alleles
mc <- GenomicRanges::mcols(gr) 
al <- data.frame(ref = mc$REF, alt = unlist(mc$ALT))
rm(mc)

# Convert {01} into {ATCG}, define minor allele and count it
geno <- plyr::ldply(1:nrow(g), function(i) {
  
  ref <- al[i, "ref"]
  alt <- al[i, "alt"]
  
  t <- gsub(pattern = "0", replacement = ref, g[i, ]) %>% 
    gsub(pattern = "1", replacement = alt)
  
  tt <- strsplit(t, "|") 
  
  n <- c(sum(grepl(pattern = ref, unlist(tt))), 
         sum(grepl(pattern = alt, unlist(tt))))
  names(n) <- c(ref, alt)
  
  if (n[1] == n[2]) {
    mall <- names(n[2])
  } else {
    mall <- names(which(n == min(n)))
  }
  
  sapply(tt, function(x) sum(grepl(pattern = mall, x)))

})

rownames(geno) <- rownames(g)
geno <- t(geno)

data.table::fwrite(geno, sprintf("%s/%s.geno", output, id), 
                   col.names = T, sep = " ", verbose = F)


