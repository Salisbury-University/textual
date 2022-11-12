import json
import pandas as pd
import multiprocessing as mp
import csv
import requests 

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

def read_data(input_file): 

    reviews = []

    client = get_client()

    db = get_database(client)

    collection = db.AmazonReviews

    with open(input_file) as tsv:
        reader = csv.DictReader(tsv, dialect="excel-tab")

        for row in reader:
            reviews.append(row)


        json_review = json.dumps(reviews, indent=4)

        collection.insert_one(json_review)

if __name__ == "__main__":

    url = 'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_multilingual_US_v1_00.tsv.gz' 
    r = requests.get(url, allow_redirects=True)

    open('amazon_reviews.tsv', 'wb').write(r.content)

    #read_data("amazon_reviews_multilingual_US_v1_00.tsv")
            
