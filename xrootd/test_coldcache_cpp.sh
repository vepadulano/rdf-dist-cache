#! /bin/bash

# usage: bash test_coldcache.sh EXECUTABLE USER HOST CACHEDIR
EXECUTABLE=$1
USER=$2
HOST=$3
CACHEDIR=$4

for i in {1..1000}
do
   printf "\nRunning $EXECUTABLE $i - coldcache\n"
   python $EXECUTABLE
   ssh -l $USER $HOST "rm -rf ${CACHEDIR}/*"
done
