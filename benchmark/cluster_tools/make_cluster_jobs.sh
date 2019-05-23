#!/bin/bash

sesame_bm_root="$(git rev-parse --show-toplevel)/benchmark"
data_dir="$sesame_bm_root/data"
genomes_fname="$data_dir/genomes.txt"
cluster_dir="$sesame_bm_root/cluster_tools"
Lvals="$data_dir/Lvals.txt"
pvals="$data_dir/pvals.txt"

# one constant to bind them all
N=50000000

# parse the genomes file
while read line; do

  # parse the input file
  set -- $line
  genome_url=$1
  md5sums_url=$2

  # parse the name of the genome file, by removing URL and gz extension, if any
  genome_file=${genome_url##*/}
  genome_file=${genome_file%%.gz}
  genome_name=${genome_file%%.fasta}
  genome_name=${genome_name%%.fna}

  # generate the directory of the genome and of the random sequences
  genome_dir=$data_dir/genomes/$genome_name
  random_sequences_dir=$genome_dir/random_sequences

  # generate random sequences cluster scripts
  pbs_random_sequences_in="$cluster_dir/randseq.pbs.in"
  for L in $(cat $Lvals); do
    for p in $(cat $pvals); do 
      pbs_random_sequences_out="$random_sequences_dir/randseq-$L-$p.pbs"
      echo $pbs_random_sequences_out

      cat $pbs_random_sequences_in |\
	sed -e s,@N@,$N,g |\
	sed -e s,@L@,$L,g |\
	sed -e s,@P@,$p,g |\
	sed -e s,@OUTFILE@,"$genome_name-$N-$L-$p.fasta",g |\
      tee > $pbs_random_sequences_out

    done
  done

done < $genomes_fname
