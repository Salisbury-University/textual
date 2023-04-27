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

# send data to the database
def send_data(headlines):

    client = get_client()
    db = get_database(client) 
    collection = db.ABC_Australia

    for i in range(len(headlines)):

        print("Thread: " + str(mp.current_process()) + " | iteration: " + str(i))
        collection.insert_one(headlines[i])

    close_database(client)

if __name__ == "__main__":

    df = pd.read_csv('abcnews-date-text.csv')
    
    headlines = [] 

    for i in range(len(df)): 

        line = (df.loc[i]).tolist()
    
        headlines.append({'date':str(line[0]), 'headline':str(line[1])})

    headline_array = np.array_split(headlines, mp.cpu_count()) 

    pool = mp.Pool(mp.cpu_count())

    pool.map(send_data, [headline for headline in headline_array])

    pool.close() 


