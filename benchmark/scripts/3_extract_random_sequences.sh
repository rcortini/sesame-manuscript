#!/bin/bash

source scripts/0_environment.sh

genomes="data/genomes.txt"

# check for proper invocation
if [ $# -ne 3 ]; then
  echo "Usage: $0 <N> <L> <mutation_rate>"
  exit 1
fi

# get parameters from command line
N=$1
L=$2
mutation_rate=$3

while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  genome_file=data/${genome_url##*/}

  # remove the ".gz" extension
  genome_file=${genome_file%%.gz}

  # build output file name
  output_file=$genome_file-$N-$L-$mutation_rate.fasta

  # extract random sequences according to preferences
  log_message "Extracting $N sequences ($L long) from $genome_file with mutation rate $mutation_rate"
  python3 scripts/extract_random_sequences.py $genome_file $N $L $mutation_rate $output_file

done < $genomes
