#! /usr/bin/bash

# usage: bash test_coldcache.sh EXECUTABLE CACHEDIR
EXECUTABLE=$1
CACHEDIR=$2

for i in {1..1000}
do
   printf "\nRunning $EXECUTABLE $i - coldcache\n"
   python $EXECUTABLE
   rm -rf $CACHEDIR/*
done
