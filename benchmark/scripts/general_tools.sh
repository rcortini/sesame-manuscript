#!/bin/bash

function generate_mapper_string {
  genome_name="$1"
  genome_fasta="$2"
  read_fasta="$3"
  sam="$4"
  mapper_command="$5"
  p="$6"
  # echo $genome_name $genome_fasta $read_fasta $mapper_command
  echo $mapper_command |\
    sed -e s,@genomename@,"$genome_name",g |\
    sed -e s,@genomefasta@,"$genome_fasta",g |\
    sed -e s,@readfasta@,"$read_fasta",g |\
    sed -e s,@sam@,"$sam",g |\
    sed -e s,@p@,"$p",g |\
  tee
}

# get directory names
sesame_bm_root="$(git rev-parse --show-toplevel)/benchmark"
data_dir="$sesame_bm_root/data"
input_makefiles_dir="$sesame_bm_root/input_makefiles"
input_conf_dir="$sesame_bm_root/input_conf"
genomes_fname="$input_conf_dir/genomes.txt"
mappers_fname="$input_conf_dir/mappers.txt"
Lvals="$input_conf_dir/Lvals.txt"
pvals="$input_conf_dir/pvals.txt"
membenchmark_dir="$data_dir/membenchmark"

# one constant to bind them all
N=50000000


