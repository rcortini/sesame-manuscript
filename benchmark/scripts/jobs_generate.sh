#!/bin/bash

function generate_mapper_string {
  genome_name="$1"
  genome_fasta="$2"
  read_fasta="$3"
  sam="$4"
  mapper_command="$5"
  # echo $genome_name $genome_fasta $read_fasta $mapper_command
  echo $mapper_command |\
    sed -e s,@genomename@,"$genome_name",g |\
    sed -e s,@genomefasta@,"$genome_fasta",g |\
    sed -e s,@readfasta@,"$read_fasta",g |\
    sed -e s,@sam@,"$sam",g |\
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

# one constant to bind them all
N=50000000

# parse the genomes file
genomes=""
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
  genome_name=${genome_name%%.fa}

  # generate the directory of the genome
  genome_dir=$data_dir/genomes/$genome_name
  mkdir -p $genome_dir

  # generate the directory of the random sequences
  random_sequences_dir=$genome_dir/random_sequences
  mkdir -p $random_sequences_dir

  # generate random sequences makefile
  makefile_random_sequences_in="$input_makefiles_dir/Makefile.random_sequences"
  makefile_random_sequences_out="$random_sequences_dir/Makefile"
  all_fasta_files=""
  cat $makefile_random_sequences_in > $makefile_random_sequences_out
  for L in $(cat $Lvals); do
    for p in $(cat $pvals); do 
      fasta_file="$genome_name-$N-$L-$p.fasta"
      all_fasta_files="$all_fasta_files $fasta_file"
      echo "" >> $makefile_random_sequences_out
      echo "$fasta_file : ../$genome_file" >> $makefile_random_sequences_out
      echo -e "\tpython3 \$(EXTRACT_RANDOM_SEQUENCES) \$^ $N $L $p \$@" >> $makefile_random_sequences_out
    done
  done
  sed -i s,@SESAME_BM_ROOT@,$sesame_bm_root,g $makefile_random_sequences_out
  sed -i s,@ALL_FASTA_FILES@,"$all_fasta_files",g $makefile_random_sequences_out

  # parse the mappers file
  old_IFS=$IFS
  IFS=$'\t'
  mappers=""
  while read mapper mapper_index mapper_map mapper_idx; do

    # generate the directory of the mapper
    mapper_dir=$genome_dir/$mapper
    mkdir -p $mapper_dir

    # generate the strings for the mapper
    mapper_index_command=$(generate_mapper_string $genome_name "\$(SYMLINK)" "\$<" "" "$mapper_index")
    mapper_map_command=$(generate_mapper_string $genome_name "\$(SYMLINK)" "\$<" "\$@" "$mapper_map")
    mapper_index_name=$(generate_mapper_string $genome_name $genome_file "" "" "$mapper_idx")

    # now make the mappers makefiles
    makefile_mappers_in="$input_makefiles_dir/Makefile.mappers"
    makefile_mappers_out="$mapper_dir/Makefile"
    cat $makefile_mappers_in |\
      sed -e s,@SESAME_BM_ROOT@,$sesame_bm_root,g |\
      sed -e s,@GENOME_FILE@,$genome_file,g |\
      sed -e s,@MAPPER@,$mapper,g |\
      sed -e s,@MAPPER_INDEX_COMMAND@,"$mapper_index_command",g |\
      sed -e s,@MAPPER_MAP_COMMAND@,"$mapper_map_command",g |\
      sed -e s,@MAPPER_INDEX@,"$mapper_index_name",g |\
      sed -e s,@ALL_FASTA_FILES@,"$all_fasta_files",g |\
    tee > $makefile_mappers_out

    # update the mappers list
    mappers="$mappers $mapper"
  done < $mappers_fname
  IFS=$old_IFS

  # generate genome makefile
  makefile_genome_in="$input_makefiles_dir/Makefile.genome"
  makefile_genome_out="$genome_dir/Makefile"
  cat $makefile_genome_in |\
    sed -e s,@SESAME_BM_ROOT@,$sesame_bm_root,g |\
    sed -e s,@GENOME_URL@,$genome_url,g |\
    sed -e s,@GENOME_FILE@,$genome_file,g |\
    sed -e s,@MD5_SUM_URL@,$md5sums_url,g |\
    sed -e s,@MAPPERS@,"$mappers",g |\
  tee > $makefile_genome_out

  # add this genome to the genome list
  genomes="$genomes $genome_name"

done < $genomes_fname

# make master Makefile
makefile_master_in=$input_makefiles_dir/Makefile.master
makefile_master_out=$data_dir/genomes/Makefile
cat $makefile_master_in |\
  sed -e s,@GENOMES@,"$genomes",g |\
tee > $makefile_master_out
