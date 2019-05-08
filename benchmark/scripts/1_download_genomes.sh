#!/bin/bash

source scripts/0_environment.sh

cd data
genomes="genomes.txt"

while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  md5sums_url=$2

  # the name of the file that we're downloading
  genome_file=${genome_url##*/}
  md5sums_file=${md5sums_url##*/}

  # get the genome
  wget --no-verbose --show-progress $genome_url -O $genome_file

  # get the md5sum file
  wget --no-verbose --show-progress $md5sums_url -O $md5sums_file

  # do the md5sum check
  grep $genome_file $md5sums_file | md5sum -c -

  if [ $? -ne 0 ]; then
    echo "ERROR: Corrupt file $genome_file" 1>&2
    exit 1
  fi

  # unzip
  gunzip $genome_file

  # log
  log_message "Downloaded and extracted $genome_file"

done < $genomes
cd ..
