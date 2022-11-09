# Yelp Review Data Collector
The documentation on the usage of the Yelp review dataset can be found at https://www.yelp.com/dataset. The data in the dataset will be formatted and written to our MongoDB database.
<br/>

# Purpose
This script will take a JSON file from the Yelp Review Dataset and write it to the MongoDB database. This requires converting each line of the file into a JSON object. The process is parallelized, with each thread doing a share of the total documents. The files are then converted into Python dictionaries to be written to the database.
<br/>

# Usage
Simply pass the desired JSON file in as a command line argument.
NOTE: Since when files are opened in Python, they are fully loaded into memory, the script can only be run with a file and machine with matching capabilities.
