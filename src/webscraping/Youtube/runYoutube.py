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

"""
This python script runs the youtube scraper continuously running it every day
"""
if __name__=='__main__':
    # run loop continuously
    database=get_database(get_client())
    while True:
        try:
            video_stat = database.command("collStats","YoutubeVideo")["freeStorageSize"]
            comment_stat = database.command("collStats","YoutubeComment")["freeStorageSize"]
            if video_stat==0 or comment_stat==0:
                print("Collection Full!\nScraper Terminated")
                close_database(database)
                break
            try:
                # runs the YouTubeComments scraper
                os.system("python3 YoutubeComments.py")
            except:
                print("\nProgram Failed")
                break
            sleep(86400) # this sleep  makes sure it is only run every day
        except:
            print("\nScraper Terminated")
            break
