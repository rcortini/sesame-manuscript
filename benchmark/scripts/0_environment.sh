function time_string {
  echo "[`date +"%Y-%m-%d %H:%M:%S"`]"
}

function log_message {
  echo "`time_string` `basename $0`: INFO: $1"
}

function error_message {
  echo "`time_string` `basename $0`: ERROR: $1" 1>&2
}
