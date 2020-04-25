#!/bin/bash

. dump.sh


for i in $(seq 1 10)
do
    while read line; do
        echo $line
        caponion "$line" $i
    done < crawl/good-onions.txt
    echo "DONE WITH ITERATION $i"
done

chown -R $USER:users $CAPDIR
