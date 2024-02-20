#!/usr/bin/perl
# Subset SNPs in the gene from Plink binary format, filter by MAF
# The output files are created in the working folder
# The file with resources (res.cfg) should be at the same folder as the script
# The file with genes is given as xls(x) file.
# Author: Gennady Khvorykh, info@inzilico.com
use strict; use warnings;
use Spreadsheet::Read qw(ReadData);
use Data::Dumper qw(Dumper);
use File::Basename;
use Getopt::Long;

# Initiate variables
my $maf = 0.10;
my $pad = 5000;
my $pref; # path/to/prefix.{bed,bim,fam}
my $xls; # path/to/filename.xls(x) with genomic coordinates of regions
my $cfg = "res.cfg";

# Parser command line arguments 
GetOptions(
	"m|maf=f" => \$maf,
	"p|pad=i" => \$pad,
	"pref=s" => \$pref,
	"xls=s" => \$xls
) or die("Error in command line arguments");

# Get working folder of the script
my $dirname = dirname(__FILE__);
my %path = read_resources("$dirname/$cfg");

# Check input
help() unless defined $xls;
help() unless defined $pref;

check_file($xls);
for my $ext ('bed', 'bim', 'fam') {
	check_file("$pref.$ext");
}

# Show input
print "xls: $xls\npref: $pref\n";
print "maf: $maf\npad: $pad\n";

# Load data
my $reg = ReadData($xls);
my @rows = Spreadsheet::Read::rows($reg->[1]);

# Skip the header 
my $head = $rows[0];
my $last = @{$head} - 1;

# Loop throug all left records and subset the SNPs
foreach my $i (1 .. $#rows) {
	next unless defined $rows[$i][5];  
	subset ($rows[$i][5], $rows[$i][7], $rows[$i][8]-$pad, $rows[$i][9]+$pad);
}

sub subset {
	# Get arguments
  	my ($gene, $chr, $start, $end) = @_;
  	# Subset SNPs by region and MAF
	print "Subsetting $gene $chr:$start-$end\n";
	my $cmd = "$path{plink} --bfile $pref --chr $chr --from-bp $start --to-bp $end --maf $maf --nonfounders --make-bed --out $gene";
	system($cmd) == 0 or die "Failed to subset SNPs by region and MAF!";
	# Output allele frequncies
	$cmd = "$path{plink} --bfile $gene --freq --nonfounders --out $gene";
	system($cmd) == 0 or die("Failed to count allele frequencies!");
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

sub check_file {
	my $file = $_[0];
	unless (-e $file) {
		print "$file doesn't exist\n";
		exit 0;
	}
}

sub help {
	print "help\n";
	exit 0;
}