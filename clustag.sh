#!/bin/bash
# Wrapper script to run clustag tool
# Should be launched from the folder with maf/r2 files 

help=$(cat << EOF

Usage: `basename $0` id
	id: sample id

EOF
)

# Check input
[ -z $1 ] && { echo "Missing arguments... $help"; exit 1; } 

# Initiate
id=$1
res="res.cfg"
declare -A tools

# Show input
echo "clustag"
echo "Sample: $id"

# Load resources
while IFS=',' read tool path; do 
  tools[${tool}]=${path}
done < $(dirname "$0")/${res}

# Create directory for output
[ ! -d out ] && mkdir out
[ ! -d temp ] && mkdir temp

# Run clustag
java -cp ${tools[clustag]}/TaggingsetChooser.jar:mail.jar \
  -d64 -Xms512m -Xmx4g \
  hk.hku.csis.biosphere.algorithm.TaggingSetChooser \
  sim=hk.hku.csis.biosphere.similarityscore.SimilarityMatrix \
  link=C \
  threshold=0.8 \
  data=${id}.data \
  corr=${id}.r2 \
  pos=${id}.maf \
  result=out/${id}.txt \
  map=out/${id}.html \
  scale=1000 \
  mem=out/${id}.members > out/${id}.out
