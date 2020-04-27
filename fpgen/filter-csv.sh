#!/bin/bash -e

ONION=$1

if [ -z $ONION ]
then
    echo Please specify onion to search for
    exit 1
fi

echo "Filtering for $ONION"

mkdir -p fingerprints/$ONION

lines=$(cat fingerprints/iat0.csv | grep $ONION | wc -l)

if [ $lines -le 0 ]
then
    echo "Onion not found"
    exit 1
fi

function filterfile() {
    head -n1 < fingerprints/$1.csv > fingerprints/$ONION/$1.csv
    cat fingerprints/$1.csv | grep $ONION >> fingerprints/$ONION/$1.csv
    cat fingerprints/$ONION/$1.csv | ../utils/create-ts-csv.sh > fingerprints/$ONION/$1-ts.csv
    wc -l fingerprints/$1.csv
    wc -l fingerprints/$ONION/$1.csv
    wc -l fingerprints/$ONION/$1-ts.csv
}


filterfile iat0
filterfile iat1
filterfile iat2
filterfile iat3
filterfile iat3-5

filterfile iat3-40
filterfile iat2-40
filterfile iat0-40
