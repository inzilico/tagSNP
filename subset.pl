#!/usr/bin/perl
# Subset SNPs from 1000 Genomes project, filter by MAF
use strict; use warnings;
use Spreadsheet::Read qw(ReadData);
use Data::Dumper qw(Dumper);

# Initiate
my $xls = $ARGV[0]; # path/to/myfile.xls with genomic coordinates of regions
my $pad = 5000;
my $maf = 0.10;
my %path = (
  'vcftools' => '/usr/local/bin/vcftools',
  'vcf' => '~/data/1000G/CEU/vcf'
); 

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
  subset ($rows[$i][5], $rows[$i][7], $rows[$i][8]-$pad, $rows[$i][9]+$pad);
  
}

sub subset {
  # Get arguments
  my ($gene, $chr, $start, $end) = @_;
  my $vcf = "$path{vcf}/CEU.chr$chr.vcf.gz";

  # Subset SNPs by region and MAF
  print "Subsetting $gene $chr:$start-$end\n";
  my $cmd = "$path{vcftools} --gzvcf $vcf --chr $chr --from-bp $start --to-bp $end --maf $maf --recode --out $gene";

  system($cmd) == 0 or die "error: vcftools failed!";
  rename "$gene.recode.vcf", "$gene.vcf";

  # Get statistics
  $vcf = "$gene.vcf"; 
  $cmd = "$path{vcftools} --vcf $vcf --hap-r2 --out $gene";
  system($cmd) == 0 or die "error: vcftools failed!";
  $cmd = "$path{vcftools} --vcf $vcf --freq2 --out $gene";
  system($cmd) == 0 or die "error: vcftools failed!";
  #$cmd = "$path{vcftools} --vcf $vcf --geno-r2 --min-r2 0.5 --out $gene";
  #system($cmd) == 0 or die "error: vcftools failed!";
}



