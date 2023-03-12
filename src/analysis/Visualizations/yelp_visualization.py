# Project Name(s): English Contextual Baseline Database
# Program Name: yelp_visualization.py
# Date: 03/11/2023
# Description: Reads in the reviews.json file containing a large subset of the Yelp Review data dump and generates visual information explaining details regarding the dataset

# ================================================================================
# Included libraries
# Pandas: storing data
# JSON: reading json file
# ================================================================================

import pandas as pd

if __name__ == "__main__":    
    yelp_review_chunks = pd.read_csv("reviews.csv", chunksize=10000) 

    for yelp_review_chunk in yelp_review_chunks:
        print(yelp_review_chunk.head())

    print("Script done...")
