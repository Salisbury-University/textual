# Project Name(s): English Contextual Baseline Database
# Program Name: amazon_to_database.py
# Date: 4/11/2023
# Description: Read individual entries from the large dataset file
# Saving format: List of data is written to the MongoDB database

# ================================================================================
# Included libraries
# Pandas: storing data
# functools, threading, multiprocessing, and counter: Multiprocessing
# sys: used for interacting with the command line
# ================================================================================
import functools as ft
import multiprocessing as mp
import threading
import pandas as pd
import json
import numpy as np
import sys
from collections import Counter

# Used to connect to the MongoDB database
from pymongo import MongoClient

# ================================================================================
#                               DATABASE FUNTIONS
# ================================================================================

# Get authoriazation from file
def get_credentials():
    with open("mongopassword.txt", "r") as pass_file:
        # Read each line from the file, splitting on newline
        lines = pass_file.read().splitlines()
    # Close the file and return the list of lines
    pass_file.close()
    return lines

# Connect to the database
def get_client():
    # Needs to be done this way, can't push credentials to github
    # Call the get pass function to open the file and extract the credentials
    lines = get_credentials()

    # Get the username from the file
    username = lines[0]

    # Get the password from the file
    password = lines[1]
    
    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

    # Return the client
    return client

# Get the database, we are using the textual database | hardcoded currently (bad)
def get_database(client):
    return client.textual

# Important, close the database
def close_database(client):
    # Close the connection to the database
    client.close()

# Open the file and return it
def openFile(filename):
    return input_file

# Method to pull from file (Will be implemented later)
def pullReviews(input_arr):
    # Get a connection to the server
    client = get_client()
    
    # Get a database from the connection
    database = get_database(client)

    # Get a collection from the database (WikiSourceText, holds the wikisource pages, WikiSourceHTML holds html source)
    amazon_collection = database.MoreAmazon

    # Iterate through each array within the numpy array
    for i in range(0, len(input_arr)):
        # Print current thread
        print("Thread: " + str(mp.current_process()) + " | iteration: " + str(i))
        # Convert to dictionary and write to database
        
        # Rename the field for the database
        try:
            review_dict = dict(input_arr[i])
            review_dict["text"] = review_dict.pop("reviewText")
            amazon_collection.insert_one(review_dict)
        except:
            print("Key error, skipping document.")
    
    # Close the connection to the database, IMPORTANT
    client.close()

# Main method
if __name__ =="__main__":
    # Get command line argument
    if (len(sys.argv) < 2):
        print("Please enter the name of a file as a command line argument")
        sys.exit()

    # Get first command user line argument
    filename = sys.argv[1]
    
    # Holds review dictionaries
    reviews=[]
    
    # Parallelizing this part will increase the script's speed further
    # Iterate through the file and append the lines as dictionaries
    
    # Open the JSON file
    with open(filename) as input_file: 
        for line in input_file:
            # Load the line as JSON 
            json_obj = json.loads(line)
            # Append the JSON object to the end of the list
            reviews.append(json_obj)

    # Split larger array into n sub arrays where n is the number of available processors
    # This is done to allow each processor to process some of the data
    # Parallelizing this part greatly speeds up the process of writing the data to the database
    reviewArray = np.array_split(reviews, mp.cpu_count())

    # Create the multithreading pool
    pool=mp.Pool(mp.cpu_count()) 
    
    #Print information to the console to inform the user on the number of threads available
    print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(pullReviews, [reviewSublist for reviewSublist in reviewArray])
    
    #Stop threads and write output to console
    pool.close()

    # Close file
    input_file.close()
    print("Done... documents written to MongoDB database")
