#!/bin/bash

CAPDIR=${CAPDIR:-'auto-caps'}
FILES=$(find $CAPDIR -type f -name "*.cap")
for f in $FILES
do
    ./analyze.py $f --noplot | grep -E "^::"
done
