import json
import pandas as pd
import multiprocessing as mp
import numpy as np
import sys
import os
import csv
from pymongo import MongoClient

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

# to read urban dictionary data to the database 
def send_data(urban_dictionary): 

    client = get_client()
    db = get_database(client)
    collection = db.UrbanDictionary

    for i in range(len(urban_dictionary)):

        print("Thread: " + str(mp.current_process()) + " | iteration: " + str(i))
        collection.insert_one(urban_dictionary[i]) 

    close_database(client) 

if __name__ == "__main__":

    cols = pd.read_csv('urbandict-word-defs.csv', nrows=1).columns
    df = pd.read_csv('urbandict-word-defs.csv', usecols=cols)

    entries = [] 

    for i in range(len(df)): 

        line = (df.loc[i]).tolist() 
        entries.append({'text':[str(line[1]), str(line[5])],'author':str(line[4]), 'word_id':str(line[0])})

    entries_array = np.array_split(entries, mp.cpu_count())

    pool = mp.Pool(mp.cpu_count())
    pool.map(send_data, [entry for entry in entries_array]) 
    pool.close() 
