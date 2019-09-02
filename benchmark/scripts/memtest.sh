#!/bin/bash

exit_script() {
    echo "Signal caught"
    trap - SIGINT SIGTERM # clear the trap
    kill -- -$$ # Sends SIGTERM to child/sub processes
}

function checkmemory {

  if [ $# -ne 2 ]; then
    return 1
  fi

  # get pid from function arguments
  mainpid=$1
  outfile=$2
  myuser=$(whoami)

  # initialize the file to know what time it is
  time_now=$(date +"%s")
  echo "$time_now 0" > $outfile

  # start an infinite loop that stops when the process is over
  while [ 1 ]
  do

    # check that the process actually exists
    ps --pid $mainpid &> /dev/null
    if [ $? -ne 0 ]; then
      return
    fi

    # put the memory footprint in file
    let memfootprint=0
    for pid in $(ps -o pid,ppid -u $myuser | grep $mainpid | awk '{ print $1 }'); do
      fp=$(ps -o rss $pid | tail -n 1)

      # the process might have stopped in the meanwhile
      if [ "$fp" == "RSS" ]; then
	fp=0
      fi

      let memfootprint=fp+memfootprint
    done
    time_now=$(date +"%s")
    echo "$time_now $memfootprint" >> $outfile

    # check every second
    sleep 1

  done
}

do_map() {
  the_command=$1
  $the_command
}

trap exit_script SIGINT SIGTERM

# invoke the command
outfile=$1
mycommand="${@:2}"
do_map "$mycommand" &
mypid=$!

# check memory
checkmemory $mypid $outfile
