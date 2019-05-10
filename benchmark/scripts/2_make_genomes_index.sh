#!/bin/bash

source 0_environment.sh

genomes="data/genomes.txt"

while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  genome_file=data/${genome_url##*/}

  # remove the ".gz" extension
  genome_file=${genome_file%%.gz}

  # make the bwa index
  log_message "Making BWA index"
  bwa index $genome_file

  # make my index
  log_message "Making my index"
  python3 scripts/make_my_genome_index.py $genome_file

done < $genomes
