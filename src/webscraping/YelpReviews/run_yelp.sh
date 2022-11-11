#!/bin/bash

i=0

for arg in "$@"
do
	python3 readYelp.py "$arg"
	echo "ITERATION $i"
	let "i=i+1"
done

echo "DONE!"
