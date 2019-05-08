#!/bin/bash

genomes="../data/genomes.txt"

cd ../data
while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  genome_file=${genome_url##*/}

  # make the bwa index
  bwa index $genome_file

done < $genomes
cd ../scripts
