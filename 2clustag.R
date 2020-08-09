#!/usr/bin/Rscript
## Transform frq/hap.ld/vcf files created by vcftools into maf/r2 files for clustag
## Usage: 2clustag.R in out
##      in: path/to/prefix of prefix.{frq,hap.ld,vcf} files.
##      out: path/to/folder to save the results
suppressPackageStartupMessages(require(dplyr, quietly = T)) 

args <- commandArgs(TRUE)

# TODO: comment after debugging
# args <- vector("character")
# args[1] <- "ADCY5"

# Check input
if(length(args) < 2) stop("Missing arguments...", call. = F)

# Initiate
id <- basename(args[1])
frq <- sprintf("%s.frq", args[1])
ld <- sprintf("%s.hap.ld", args[1])
vcf <- sprintf("%s.vcf", args[1])
output <- args[2]

# Check input
if(!file.exists(frq)) stop(sprintf("file %s doesn't exist!", frq), call. = F)
if(!file.exists(ld)) stop(sprintf("file %s doesn't exist!", ld), call. = F)
if(!file.exists(vcf)) stop(sprintf("file %s doesn't exist!", vcf), call. = F)

# Load frequencies
d1 <- data.table::fread(frq, header = F) %>% select(pos = V2, ref = V5, alt = V6)
# Count MAF
d1$maf <- apply(d1, 1, function(x) min(x["ref"], x["alt"]))

# Load SNP ids
cmd <- paste("bcftools query -f '%CHROM %POS %ID %REF %ALT\n'", vcf)
t <- system(cmd, intern = T)
snps  <- stringr::str_split(t, " ", simplify = T) %>%
  data.table::as.data.table() %>% 
  select(rs = V3, pos = V2)
snps[, pos := as.numeric(pos)]

# Merge by pos
data.table::setkey(d1, pos)
data.table::setkey(snps, pos)
d2 <- snps[d1, nomatch = 0]

# Save file wih MAF
if(!dir.exists(output)) dir.create(output, recursive = T) 
data.table::fwrite(d2[, .(rs, pos, maf)], paste0(output, "/", id, ".maf"), 
                   sep = " ", col.names = F)

message("Sample: ", id)
message("No of SNPs: ", nrow(d2))
message(sprintf("min/max MAF: %s %s", 
                round(min(d2$maf), 3), 
                round(max(d2$maf), 3)))

# Load data with LD
d3 <- data.table::fread(ld) %>% select (pos1 = POS1, pos2 = POS2, r2 = 'R^2')

# Replace 'pos' for 'rs' values
pos2rs <- function(x) {
  sapply(x, function(y) snps$rs[snps$pos == y])
}
d3$rs1 <- pos2rs(d3$pos1)
d3$rs2 <- pos2rs(d3$pos2)

# Save file with R^2
data.table::fwrite(d3[, .(rs1, rs2, r2)], paste0(output, "/", id, ".r2"), 
                   sep = " ", col.names = F)

