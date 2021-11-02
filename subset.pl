#!/usr/bin/perl
# Subset SNPs from 1000 Genomes project, filter by MAF
# The outpup files are created in the working folder
# The file with resources (res.cfg) should be at the same folder as the script
# Author: Gennady Khvorykh, info@inzilico.com
use strict; use warnings;
use Spreadsheet::Read qw(ReadData);
use Data::Dumper qw(Dumper);
use File::Basename;
use Getopt::Long;

# Initiate
my $ch;
GetOptions(
	"c|chr" => \$ch
) or die("Error in command line arguments");

my $xls = $ARGV[0]; # path/to/myfile.xls(x) with genomic coordinates of regions
my $pad = 5000;
my $maf = 0.10;
my $cfg = "res.cfg";
my $dirname = dirname(__FILE__);
my %path = read_resources("$dirname/$cfg");

# Show input
print "Input: $xls\n";

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
  my $vcf = "$path{vcf}/CEU.chr$chr.vcf.gz";
	return unless -e $vcf;

	# Correct chromosome id if required
	$chr = "chr${chr}" if $ch;

  # Subset SNPs by region and MAF
  print "Subsetting $gene $chr:$start-$end\n";
  my $cmd = "$path{vcftools} --gzvcf $vcf --chr $chr --from-bp $start --to-bp $end --maf $maf --recode --out $gene";

  system($cmd) == 0 or die "error: vcftools failed!";
  rename "$gene.recode.vcf", "$gene.vcf";
	
	# Get the number of variants
	my $n = `grep -cv "^#" $gene.vcf`;
	chomp $n;
	return if $n == 0;

  # Get statistics
  $vcf = "$gene.vcf"; 
  $cmd = "$path{vcftools} --vcf $vcf --hap-r2 --out $gene";
  system($cmd) == 0 or die "error: vcftools failed!";
  $cmd = "$path{vcftools} --vcf $vcf --freq2 --out $gene";
  system($cmd) == 0 or die "error: vcftools failed!";
  #$cmd = "$path{vcftools} --vcf $vcf --geno-r2 --min-r2 0.5 --out $gene";
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

