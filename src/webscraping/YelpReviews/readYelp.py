# Project Name(s): English Contextual Baseline Database
# Program Name: readYelp.py
# Date: 11/9/2022-...
# Description: Read individual entries from the large dataset file
# Saving format: List of data is written to the MongoDB database

# ================================================================================
# Included libraries
# Pandas: storing data
# functools, threading, multiprocessing, and counter: Multiprocessing
# JSON: reading json file
# ================================================================================
import functools as ft
import multiprocessing as mp
import threading
import pandas as pd
import json
from collections import Counter

# Open the file and return it
def openFile(filename):
    input_file = open(filename)
    return input_file

# Method to pull from file (Will be implemented later)
def pullReviews(input_str):
    
    print (input_str)
    # Print current thread
    print("Thread: " + str(mp.current_process()))

# Main method
if __name__ =="__main__":
    # Open the JSON file
    input_file = openFile("yelp_academic_dataset_business.json")
    
    # Holds review dictionaries
    reviews=[]

    # Iterate through the file and append the lines as dictionaries
    for line in input_file:
        json_obj = json.loads(line)
        reviews.append(json_obj)

    # Create the multithreading pool
    pool=mp.Pool(mp.cpu_count())
    
    #Write the pages to the list
    reviewList=[]
    for i in range(mp.cpu_count()):
        reviewList.append(reviews[i])
    
    #Print information to the console to inform the user on the number of threads available
    print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(pullReviews, [reviewEntry for reviewEntry in reviewList])
    
    #Stop threads and write output to console
    pool.close()

    # Close file
    input_file.close()
    print("Done... pulled files written to MongoDB database")
