#!/bin/bash

dir="./reviews/"
i=0

for file in "$dir"*
do
	echo "Iteration: $i"
	let i=i+1

	if [ -f "$file" ]; then
		python3 google_to_database.py "$file"		
	fi
done

exit
