#!/bin/bash

if [ -z "$2" ]
then
    echo "No destination!"
    exit 1
fi

echo "Source: $1"
echo "Dest:   $2"


nstr="$(ls $1 -1 | colrm 17 | sort | uniq)"
names=(${nstr// / })

for i in ${!names[@]}
do
    n="${names[$i]}"
    echo $i $n
    files=$(cd $1; ls -r $n*)
    for f in $files
    do
        nf=$(echo $f | sed -e "s/$n.*.onion/$i/" -e "s/.pcap.*//")
        echo "./analyze.py $1/$f --batchgen > $2/$nf"
        ./analyze.py $1/$f --batchgen > $2/$nf
    done
done
