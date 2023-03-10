import pymongo as db
import sys
from time import sleep
import os

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

# run loop continuously
"""
I added some error catching just for a clear place where it failed or was interrupted by the user.
"""
while True:
    try:
        sub_reddits=""
        with open("subreddit.txt","r") as fd: # open file with some popular subreddits (PG-13 of course)
            next_line=fd.readline()
            while next_line!="":
                sub_reddits+=next_line[:-1]
                next_line=fd.readline()
                # Just a check for the last item in the file and adjusts accordingly
                if next_line=="":
                    sub_reddits+="w"
                else:
                    sub_reddits+=" "
        database=get_database(get_client())
        collection_stats = database.command("collStats","RedditPosts")
        if collection_stats.freeStorageSize==0:
            print("Collection Full!\nScraper Terminated")
            close_database(database)
            break
        try:
            # runs the reddit scraper
            os.system("python3 readRedditDBParallel_V2" + sub_reddits)
        except:
            print("\nProgram Failed")
            close_database(database)
            break
        sleep(20) # this sleep  makes sure it is only run every day
    except:
        print("\nScraper Terminated")
        close_database(database)
        break
