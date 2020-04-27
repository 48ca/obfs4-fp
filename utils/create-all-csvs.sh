#!/bin/bash -x

pushd ..

. env.sh

cd fpgen

CAPDIR=dumps/15/IAT0 ./csv-gen.sh   > fingerprints/iat0.csv
CAPDIR=dumps/15/IAT1 ./csv-gen.sh   > fingerprints/iat1.csv
CAPDIR=dumps/15/IAT2 ./csv-gen.sh   > fingerprints/iat2.csv
CAPDIR=dumps/15/IAT3 ./csv-gen.sh   > fingerprints/iat3.csv
CAPDIR=dumps/15/IAT3-5 ./csv-gen.sh > fingerprints/iat3-5.csv
CAPDIR=dumps/40/IAT0 ./csv-gen.sh   > fingerprints/iat0-40.csv
CAPDIR=dumps/40/IAT2 ./csv-gen.sh   > fingerprints/iat2-40.csv
CAPDIR=dumps/40/IAT3 ./csv-gen.sh   > fingerprints/iat3-40.csv

popd
