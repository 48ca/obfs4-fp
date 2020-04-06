#!/bin/bash -eu

FP="$1"

ACC="0"
ITERS=10

for i in `seq $ITERS`
do
    a="$(./classify.py $FP | grep "Accuracy" | cut -d' ' -f2)"
    if [[ $a > $ACC ]]
    then
        ACC=$a
        set -x
        echo "Updated accuracy to $ACC"
        cp models/$FP-randomforest.sav auto-good-models/$FP-randomforest.sav
        set +x
    fi
done

echo "Finally accuracy: $ACC"
