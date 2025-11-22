#!/usr/bin/perl
# Subset SNPs from 1000 Genomes project, filter by MAF
# The output files are created in the working folder
# The file with resources (res.cfg) should be at the same folder as the script
# Author: Gennady Khvorykh, info@inzilico.com
use strict; use warnings;
use Spreadsheet::Read qw(ReadData);
use Data::Dumper qw(Dumper);
use File::Basename;
use Getopt::Long;

# Initiate
my $ch;
my $maf = 0.10;
my $pad = 5000;
GetOptions(
	"c|chr" => \$ch,
	"m|maf=f" => \$maf,
	"p|pad=i" => \$pad
) or die("Error in command line arguments");

my $xls = $ARGV[0]; # path/to/myfile.xls(x) with genomic coordinates of regions
my $cfg = "res.cfg";
my $dirname = dirname(__FILE__);
my %path = read_resources("$dirname/$cfg");

# Check input
unless (defined $xls) {
	print "path/to/file.xls isn't defined\n";
	exit 0;
}	

if (! -e $xls ) {
	print "$xls doesn't exist\n" ;
	exit 1;
}

# Show input
print "Input: $xls\n";
print "maf: $maf\npad: $pad\n";

# Load data
my $reg = ReadData($xls);
my @rows = Spreadsheet::Read::rows($reg->[1]);

# Loop throug all records and subset the SNPs
# The header is skipped
my $head = $rows[0];
my $last = @{$head} - 1;

foreach my $i (1 .. $#rows) {
	next unless defined $rows[$i][5];  
	subset ($rows[$i][5], $rows[$i][7], $rows[$i][8]-$pad, $rows[$i][9]+$pad);
}

sub subset {
	# Get arguments
	my ($gene, $chr, $start, $end) = @_;

	# Assign variables
	my $vcf1 = "$path{vcf}/CEU.chr$chr.vcf.gz";
	my $vcf2 = "$gene.vcf";

	# Check input file exists
	return unless -e $vcf1;

	# Correct chromosome id if required
	$chr = "chr${chr}" if $ch;

	# Subset SNPs by region and MAF
	print "Subsetting $gene $chr:$start-$end\n";
	my $cmd = "$path{vcftools} --gzvcf $vcf1 --chr $chr --from-bp $start --to-bp $end --maf $maf --recode --out $gene";
	system($cmd) == 0 or die "error: vcftools failed!";
	rename "$gene.recode.vcf", $vcf2;
	
	# Get the number of variants subsetted 
	my $n = `grep -cv "^#" $vcf2`;
	chomp $n;
	print "Number of variants: $n\n";
	return if $n == 0;

	# Estimate r2
	if ($n > 1) {
		$cmd = "$path{vcftools} --vcf $vcf2 --hap-r2 --out $gene";
		system($cmd) == 0 or die "error: vcftools failed!";
	}

	# Estimate frequencies
	$cmd = "$path{vcftools} --vcf $vcf2 --freq2 --out $gene";
	system($cmd) == 0 or die "error: vcftools failed!";
	
	#$cmd = "$path{vcftools} --vcf $vcf2 --geno-r2 --min-r2 0.5 --out $gene";
	#system($cmd) == 0 or die "error: vcftools failed!";
}

sub read_resources {
	my $res = $_[0];
	# Check input
	die "$res doesn't exist!" unless -e $res;
	my $fh;
	my %path;
	open($fh, '<', $res);
	while(<$fh>) {
		chomp $_;
		my @ar = split /,/;
		$path{$ar[0]} = $ar[1];
	}
	close $fh;
	return %path;
}

