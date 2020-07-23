#! /bin/bash

# usage: bash test_coldcache.sh EXECUTABLE USER HOST CACHEDIR
EXECUTABLE=$1
USER=$2
HOST=$3
CACHEDIR=$4

for i in {1..100}
do
   echo "Running $EXECUTABLE $i - coldcache"
   ./$EXECUTABLE
   ssh -l $USER $HOST "rm -rf ${CACHEDIR}/*"
done
