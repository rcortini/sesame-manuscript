#!/bin/bash

source general_tools.sh

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
  declare -a seqs
  let i=0
  for L in $(cat $Lvals); do
    for p in $(cat $pvals); do 
      seq="$genome_name-$N-$L-$p"
      fasta_file="$seq.fasta"
      all_fasta_files="$all_fasta_files $fasta_file"
      echo "" >> $makefile_random_sequences_out
      echo "$fasta_file : ../$genome_file" >> $makefile_random_sequences_out
      echo -e "\tpython3 \$(EXTRACT_RANDOM_SEQUENCES) \$^ $N $L $p \$@" >> $makefile_random_sequences_out
      seqs[i]="$seq"
      let i=i+1
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

    # generate mapper map commands
    rm -f temp
    for seq in "${seqs[@]}"; do
      fa_file="$seq.fa"
      sam_file="$seq.sam"
      membenchmark_file="$seq.membenchmark"
      p=$(echo $seq | rev | cut -d '-' -f1 | rev)
      mapper_map_command=$(generate_mapper_string $genome_name "\$(SYMLINK)" "$fa_file" "$sam_file" "$mapper_map" "$p")
      echo "$sam_file : $fa_file \$(MAPPER_INDEX)" >> temp
      echo -e "\t$mapper_map_command" >> temp
      echo "" >> temp

      mini_fa_file="$seq-mini.fa"
      mini_sam_file="$seq-mini.sam"
      mapper_membenchmark_command=$(generate_mapper_string $genome_name "\$(SYMLINK)" "$mini_fa_file" "$mini_sam_file" "$mapper_map" "$p")
      echo "$membenchmark_file : $fa_file \$(MAPPER_INDEX)" >> temp
      echo -e "\thead -n \$(N_MEMBENCHMARK) $fa_file > $mini_fa_file" >> temp
      echo -e "\tbash \$(MEMTEST) \$@ $mapper_membenchmark_command" >> temp
      echo -e "\trm -rf $mini_fa_file $mini_sam_file" >> temp
      echo "" >> temp
    done

    # now make the mappers makefiles
    makefile_mappers_in="$input_makefiles_dir/Makefile.mappers"
    makefile_mappers_out="$mapper_dir/Makefile"

    cat $makefile_mappers_in |\
      sed -e s,@SESAME_BM_ROOT@,$sesame_bm_root,g |\
      sed -e s,@GENOME_FILE@,$genome_file,g |\
      sed -e s,@MAPPER@,$mapper,g |\
      sed -e s,@MAPPER_INDEX_COMMAND@,"$mapper_index_command",g |\
      sed -e '/@MAPPER_MAP_COMMANDS@/{r temp' -e 'd}' |\
      sed -e s,@ALL_FASTA_FILES@,"$all_fasta_files",g |\
      sed -e s,@N_MEMBENCHMARK@,"$N_MEMBENCHMARK",g |\
    tee > $makefile_mappers_out
    rm -f temp

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
