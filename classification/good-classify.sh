#!/bin/bash -eu

FP="$1"

ACC="0"
ITERS=20
SQRTITERS="$(echo "scale=10;$ITERS" | bc)"

total="0"
numbers=""

for i in `seq $ITERS`
do
    a="$(./classify.py $FP | grep "Accuracy" | cut -d' ' -f2)"
    total=$(echo "scale=10;$total + $a "| bc)
    numbers="$numbers $a"
    if [[ $a > $ACC ]]
    then
        ACC=$a
        cp models/$FP-randomforest.sav auto-good-models/$FP-randomforest.sav
    fi
done

echo "$FP"
echo "Max accuracy: $ACC"

echo "Total: $total"
avg=$(echo "scale=10;$total / $ITERS" | bc)
echo "Average accuracy: $avg"

standardDeviation=$(
    echo $numbers | sed 's/ /\n/g' |
        awk '{sum+=$1; sumsq+=$1*$1}END{print sqrt(sumsq/NR - (sum/NR)**2)}'
)
echo "Std dev: $standardDeviation"
echo "Error: $(echo "scale=10;$standardDeviation/$SQRTITERS" | bc)"
