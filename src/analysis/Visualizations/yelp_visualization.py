# Project Name(s): English Contextual Baseline Database
# Program Name: yelp_visualization.py
# Date: 03/11/2023
# Description: Reads in the reviews.json file containing a large subset of the Yelp Review data dump and generates visual information explaining details regarding the dataset

# ================================================================================
# Included libraries
# Pandas: storing data
# ================================================================================

import pandas as pd
import collections
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

if __name__ == "__main__":    
    # Load csv file, minimize memory usage using chunks
    yelp_review_chunks = pd.read_csv("reviews.csv", chunksize=10000) 

    # Five lists to hold the reviews based on the number of stars
    review_stars = [ [], [], [], [], [] ]

    # 2D list to hold the most common words found in each review
    review_words = [ [], [], [], [], [] ]

    stop_words = set(stopwords.words("english"))

    # Iterate through the chunks
    for yelp_review_chunk in yelp_review_chunks:

        # Extract the review text based on the number of stars
        for index, row in yelp_review_chunk.iterrows():
            if (row["stars"] == 5.0):
                review_stars[4].append(row["text"])
            elif (row["stars"] == 4.0):
                review_stars[3].append(row["text"])
            elif (row["stars"] == 3.0):
                review_stars[2].append(row["text"])
            elif (row["stars"] == 2.0):
                review_stars[1].append(row["text"])
            else:
                review_stars[0].append(row["text"])
        
    for review_type in review_stars: 
        # Count the occurence of each word
        num_words = collections.Counter(word for word in " ".join(review_type).split() if word.lower() not in stop_words)
        most_common = num_words.most_common(10)
        
        for word, frequency in most_common:
            print(f'{word}: {frequency}')

    print("Script done...")
