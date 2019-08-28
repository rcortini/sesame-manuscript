#!/bin/bash

function checkmemory {

  if [ $# -ne 2 ]; then
    return 1
  fi

  # get pid from function arguments
  mainpid=$1
  outfile=$2
  myuser=$(whoami)

  rm -rf $outfile
  while [ 1 ]
  do

    # check that the process actually exists
    ps --pid $mainpid &> /dev/null
    if [ $? -ne 0 ]; then
      break
    fi

    # put the memory footprint in file
    let memfootprint=0
    for pid in $(ps -o pid,ppid -u $myuser | grep $mainpid | awk '{ print $1 }'); do
      fp=$(ps -o rss $pid | tail -n 1)
      let memfootprint=fp+memfootprint
    done
    time_now=$(date +"%s")
    echo "$time_now $memfootprint" >> $outfile

    # check every second
    sleep 1

  done
}

# invoke the command
outfile=$1
mycommand="${@:2}"
echo "MEMTEST executing: $mycommand"
$mycommand &
mypid=$!

# check memory
checkmemory $mypid $outfile
