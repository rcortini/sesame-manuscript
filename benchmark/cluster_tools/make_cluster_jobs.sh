#!/bin/bash

sesame_bm_root="$(git rev-parse --show-toplevel)/benchmark"
data_dir="$sesame_bm_root/data"
cluster_dir="$sesame_bm_root/cluster_tools"

input_conf_dir="$sesame_bm_root/input_conf"
genomes_fname="$input_conf_dir/genomes.txt"
mappers_fname="$input_conf_dir/mappers.txt"
Lvals=$(cat "$input_conf_dir/Lvals.txt")
pvals=$(cat "$input_conf_dir/pvals.txt")

# one constant to bind them all
N=50000000

# input PBS scripts
pbs_random_sequences_in="$cluster_dir/randseq.pbs.in"
pbs_map_in="$cluster_dir/map.pbs.in"

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
  for L in $Lvals; do
    for p in $pvals; do 
      pbs_random_sequences_out="$random_sequences_dir/randseq-$L-$p.pbs"
      pbs_map_out="$random_sequences_dir/map-$L-$p.pbs"

      cat $pbs_random_sequences_in |\
	sed -e s,@N@,$N,g |\
	sed -e s,@L@,$L,g |\
	sed -e s,@P@,$p,g |\
	sed -e s,@GENOME@,$genome_name,g |\
	sed -e s,@OUTFILE@,"$genome_name-$N-$L-$p.fasta",g |\
      tee > $pbs_random_sequences_out

      # parse the mappers file
      old_IFS=$IFS
      IFS=$'\t'
      mappers=""
      while read mapper mapper_index mapper_map mapper_idx; do

	# generate the directory of the mapper
	mapper_dir=$genome_dir/$mapper

	pbs_map_out=$mapper_dir/map-$L-$p.pbs
	cat $pbs_map_in |\
	  sed -e s,@MAPPER@,$mapper,g |\
	  sed -e s,@N@,$N,g |\
	  sed -e s,@L@,$L,g |\
	  sed -e s,@P@,$p,g |\
	  sed -e s,@GENOME@,"$genome_name",g |\
	tee > $pbs_map_out

      done < $mappers_fname
      IFS=$old_IFS

    done

  done

done < $genomes_fname
