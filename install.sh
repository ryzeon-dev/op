#!/bin/bash 

if [ "$(whoami)" != "root" ]; then
  echo "Execution requires root"
  exit 1
fi 

cp ./op /usr/local/bin
