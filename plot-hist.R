## Plot the histogram of allele frequencies
args <- commandArgs(T)
fn <- args[1]
pref <- args[2]
if(!file.exists(fn)) stop(fn, " doesn't exist", call. = F)
d <- read.table(fn, header = T, stringsAsFactors = F)
png(filename = paste0(pref, ".png"))
hist(d$MAF, breaks = seq(0, 0.5, 0.05), main = "", xlab = "MAF")
invisible(dev.off())