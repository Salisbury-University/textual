# Project Name(s): English Contextual Baseline Database
# Program Name: readYelp.py
# Date: 11/9/2022-...
# Description: Read individual entries from the large dataset file
# Saving format: List of data is written to the MongoDB database

# ================================================================================
# Included libraries
# Pandas: storing data
# functools, threading, multiprocessing, and counter: Multiprocessing
# ================================================================================
import functools as ft
import multiprocessing as mp
import threading
import pandas as pd
from collections import Counter

# Method to pull from file (Will be implemented later)
def pullReviews(input_str):
    
    # Print current thread
    print("Thread: " + str(mp.current_process()))

# Main method
if __name__ =="__main__":
    # Create the multithreading pool
    pool=mp.Pool(mp.cpu_count())
    
    #Write the pages to the list
    entryCount=[]
    for i in range(mp.cpu_count()):
        entryCount.append(20)
    
    #Print information to the console to inform the user on the number of threads available
    print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(pullReviews, [pageNum for pageNum in entryCount])
    
    #Stop threads and write output to console
    pool.close()
    print("Done... pulled files written to MongoDB database")
