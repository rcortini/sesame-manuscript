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
    sed -e s,@sam@,"$sam",g
}

function checkmemory {

  if [ $# -ne 2 ]; then
    return 1
  fi

  # get pid from function arguments
  pid=$1
  outfile=$2

  while [ 1 ]
  do

    # check that the process actually exists
    ps --pid $pid &> /dev/null
    if [ $? -ne 0 ]; then
      break
    fi

    # put the memory footprint in file
    ps -o rss $pid | tail -n 1 >> $outfile

    # check every five seconds
    sleep 5

  done
}

sesame_bm_root="$(git rev-parse --show-toplevel)/benchmark"
data_dir="$sesame_bm_root/data"
membenchmark_dir="$data_dir/membenchmark"
mappers_fname="$membenchmark_dir/mappers.txt"
in_fasta="$membenchmark_dir/mini.fasta"

# genome
genome_name="GCA_000404065.3_Ptaeda2.0_genomic"
genome_file=$genome_name.fna

# parse the mappers file
old_IFS=$IFS
IFS=$'\t'
mappers=""
root_dir=$(pwd)

cd $membenchmark_dir
while read mapper mapper_index mapper_map mapper_idx; do

  cd $mapper
  footprint_file="$mapper-memfootprint_t.dat"
  rm -f $footprint_file

  # generate the map command
  mapper_map_command=`generate_mapper_string $genome_name $genome_file $in_fasta "out.sam" "$mapper_map"`
  # echo $mapper_map_command

  eval $mapper_map_command &
  sleep 1
  pid=$(pgrep $mapper)
  echo $pid
  checkmemory $pid $footprint_file
  if [ $? -ne 0 ]; then
    echo $mapper_map_command FAILED
    break
  fi
  cd ..

done < $mappers_fname
IFS=$old_IFS
cd $root_dir
