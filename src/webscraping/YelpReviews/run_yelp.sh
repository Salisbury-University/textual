#!/bin/bash

# Iteration variable
i=0

# Loop through all the command line arguments
for arg in "$@"
do
	# Run the readYelp.py script which will write the contents of the json files to the mongoDB
	python3 readYelp.py "$arg"
	
	# Print iteration number and increment
	echo "ITERATION $i"
	let "i=i+1"
done

# Print message and exit with status 0
echo "DONE!"
exit 0
