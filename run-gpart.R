## Make blocks with gpart

tictoc::tic("Time: ")

# Check arguments
args <- commandArgs(T)
if(length(args) != 1) stop("path/to/pref is missing", call. = F)
info_file <- paste0(args[1], ".info")
geno_file <- paste0(args[1], ".geno")

# Check input
for (file in c(info_file, geno_file)) {
	if(!file.exists(file)) stop(file, " doesn't exist", call. = F) 
}

# Load data
info <- data.table::fread(info_file, colClasses = c("integer", "factor", "integer"))
geno <- data.table::fread(geno_file) 


# Construct LD blocks
blocks <- gpart::BigLD(geno = geno, SNPinfo = info, MAFcut = 0.0)

# Save output
out_file <- paste0(args[1], ".gpart")
data.table::fwrite(blocks, out_file, sep = " ")

tictoc::toc()
