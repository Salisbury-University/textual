# Project Name(s): English Contextual Baseline Database
# Program Name: mongoTest.py
# Date: 11/11/2022
# Description: Connect to the database from the HS Linux PCs

# ================================================================================
# Included libraries
# Pandas: storing data
# functools, threading, multiprocessing, and counter: Multiprocessing
# JSON: reading json file
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

# Main method
if __name__ =="__main__":
    # Get connection to client
    client = get_client()

    # Get textual database
    db = get_database(client)
    print("Connected to MongoDB!")

    # Get collection for yelp review dataset
    collection = db.YelpReviews

    # Read line from collection
    review = collection.find({"stars": 5.0}, {"text": 1})

    # Print header
    print("Review found: ", end=" ")
    
    # Print each item found
    for data in review:
        print(data)

    # Close connection to database
    client.close()

    # Ending message
    print("Done... Connection to database terminated")
