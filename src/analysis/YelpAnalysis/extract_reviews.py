# Project Name(s): English Contextual Baseline Database
# Program Name: extract_reviews.py
# Date: 11/26/2022
# Description: Reads in the Yelp Review JSON file and extracts the text and stars portion from each review
# Saving format: Output is a csv file with each review's stars and text

# ================================================================================
# Included libraries
# Pandas: storing data
# JSON: reading json file
# ================================================================================

import json
import pandas as pd

# Create new dataframe
data = pd.DataFrame()

# Iteration variable to print to the screen
i=0

# Open the JSON file
with open("reviews.json") as input_file: 
    # Iterate though each review
    for line in input_file:
        # Print a message to the console every 10000 iterations
        if i % 10000 == 0:
            print("Iteration: " + str(i))
        
        # Increase the iteration variable
        i = i + 1

        # Convert the current line to a JSON file
        json_obj = json.loads(line)
        # Extract the review text and the star rating
        # Append the review to the dataframe
        data = data.append({"stars" : json_obj["stars"], "text" : json_obj["text"]}, ignore_index=True)

# After all iterations are complete, save the reviews to a csv file
data.to_csv("reviews.csv", index=False)
