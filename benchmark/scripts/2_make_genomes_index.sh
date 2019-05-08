#!/bin/bash

genomes="data/genomes.txt"

while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  genome_file=data/${genome_url##*/}

  # remove the ".gz" extension
  genome_file=${genome_file%%.gz}

  # make the bwa index
  bwa index $genome_file

done < $genomes
