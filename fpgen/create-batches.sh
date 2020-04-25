#!/bin/bash -e

if [ -z "$2" ]
then
    echo "No destination!"
    exit 1
fi

echo "Source: $1"
echo "Dest:   $2"

nstr="$(ls $1/*.pcap -1 | colrm 17 | sort | uniq)"
names=(${nstr// / })
names="auzbdiguv5qtp37xo"

for i in ${!names[@]}
do
    n="${names[$i]}"
    echo $i $n
    files=$(cd $1; ls $n*.pcap)
    for f in $files
    do
        nf=$(echo $f | sed -e "s/$n/$i/")
        echo $f $nf
    done
done
