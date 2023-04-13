import json
import pandas as pd
import multiprocessing as mp
import numpy as np
import sys
import os
import csv
from pymongo import MongoClient

key_word = "X-Filename" 

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

# Get a database from the client
# In this case use the textual database
def get_database(client):
    return client.textual

# Close the connection to the database after data has been written
def close_database(client):
    # Close database connection
    client.close()

def read_file(path): 

    with open(path, 'r') as file_: 
        lines = file_.readlines() 

    keyword_index = None

    for i, line in enumerate(lines):
        if keyword in line: 
            keyword_index = i
            break 

    if keyword_index is None: 
        print(f'The keyword "{key_word}" was not found.') 
        sys.exit() 

    other_lines = lines[keyword_index+1] 

    # convert other_lines to a string 

    new_data_string = ' '.join(other_lines) 

    new_entry = {'text':new_data_string} 

    client = get_client() 
    db = get_database(client) 
    collection = db.EnronEmails 

    collection.insert_one(new_entry) 

