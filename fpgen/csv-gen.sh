#!/bin/bash

CAPDIR=${CAPDIR:-'auto-caps'}
FILES=$(find $CAPDIR -type f -name "*.pcap")

echo -n "name,out,in,total,outp,inp,tin,tout,retransmission,finalts"
for i in $(seq 1 1500)
do
    echo -n ",uniqnum$i"
done
for i in $(seq 1 5000)
do
    echo -n ",packetd$i"
done
echo

for f in $FILES
do
    ./analyze.py $f --noplot | grep -E "^!csv:" | cut -d" " -f2
done
