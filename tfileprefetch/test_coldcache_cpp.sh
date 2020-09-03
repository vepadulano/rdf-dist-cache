#! /usr/bin/bash

# usage: bash test_coldcache.sh EXECUTABLE CACHEDIR
EXECUTABLE=$1
CACHEDIR=$2

for i in {1..1000}
do
   echo "Running $EXECUTABLE $i - coldcache"
   ./$EXECUTABLE
   rm -rf $CACHEDIR/*
done
