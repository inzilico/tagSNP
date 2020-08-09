#!/usr/bin/Rscript
## Convert vcf files for haploview (haps) files, which are phased 
## Usage: vcf2haploview <input> <output>
##        input: path/to/mydata.vcf
##        output: path/to/folder to save the output

suppressPackageStartupMessages(require(dplyr)) 
args <- commandArgs(TRUE)

# TODO: comment after debugg
# args[1] <- "~/data/ortho/maf10/ADCY5.vcf"
# args[2] <- "~/data/ortho/maf10/hv/ADCY5"

# Check arguments provided
if(length(args) < 2) stop("Missing arguments...", call. = F)

# Initilize
vcf <- args[1]
id <- basename(vcf) %>% sub(pattern = ".vcf", replacement = "")
output <- args[2]

# Check file exists
if(!file.exists(vcf)) stop(vcf, " isn't found", call. = F)

message("Sample: ", id)

# Create folder for output if not exist
if(!dir.exists(output)) dir.create(output, recursive = T)

# Generate haps files from vcf
cmd <- sprintf("vcftools --vcf %s --IMPUTE --out %s/%s", vcf, output, id)
system(cmd)

# Load haplotypes, legend, and samples
hap <- data.table::fread(paste0(output, "/", id, ".impute.hap")) 
leg <- data.table::fread(paste0(output, "/", id, ".impute.legend"),
                         col.names = c("id", "pos", "a0", "a1"))
sam <- data.table::fread(paste0(output, "/", id, ".impute.hap.indv"),
                         header = F, col.names = "sid")

# Check the number of SNPs are equal
if(nrow(hap) != nrow(leg)) stop("The number of SNPs are different!", call. = F)

# Check the number of samples and haplotypes coincide
if(ncol(hap) != 2*nrow(sam)) stop("The number of samples and haplotypes are different!", 
                         call. = F)

message("SNPs loaded: ", nrow(leg))
message("Haplotypes loaded: ", ncol(hap))
message("Samples loaded: ", nrow(sam))

# Convert {0, 1} alleles into {A, C, G, T} 
nuc <- c("A", "C", "G", "T")
message("Converting...")
hap <- hap[, lapply(.SD, function(x) 
  ifelse(x == 0, leg[, a0], leg[, a1]))]

# Convert {A, C, G, T} into {1, 2, 3, 4} 
hap <- apply(hap, c(1,2), function(x) 
  switch(x, "A" = 1, "C" = 2, "G" = 3, "T" = 4))

# Create genotypes
gn <- matrix(mapply(paste, hap[, c(T, F)], hap[, c(F, T)]),
            nrow = nrow(hap), byrow = F)

# Transpose
#hap <- t(hap)
gn <- t(gn)

# Add extra columns required 
ped <- cbind(0, sam, 0, 0, 0, 0, gn)
# hap <- cbind(sam, sam, hap)


# Save output in standart linkage format 
data.table::fwrite(ped, sprintf("%s/%s.ped", output, id), 
 col.names = F, sep = "\t", verbose = F, quote = F)

data.table::fwrite(leg[, .(id, pos)], sprintf("%s/%s.info", output, id), 
                   col.names = F, sep = " ", verbose = F)

# Save output as phased haplotypes
# data.table::fwrite(hap, sprintf("%s/%s.haps", output, id), 
                   # col.names = F, sep = " ", verbose = F)

# data.table::fwrite(leg, sprintf("%s/%s.legend", output, id), 
                   # col.names = T, sep = " ", verbose = F)

# Clean
cmd <- sprintf("rm %s %s %s %s", 
               paste0(output, "/", id, ".impute.hap"),
               paste0(output, "/", id, ".impute.legend"),
               paste0(output, "/", id, ".impute.hap.indv"),
               paste0(output, "/", id, ".log"))

system(cmd)
