# Project Name(s): English Contextual Baseline Database
# Program Name: readReddit.py
# Date: 10/6/2022
# Description: Use the Reddit API to collect content a specified subreddit and store as a .json or .csv file

# Import required packages
import requests
import json
import requests.auth
import sys
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation
import itertools

# Used to connect to the mongo DB
from pymongo import MongoClient

# Connect to the database
def get_client():
    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000")
    
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

# Read in password from separate file
def get_pass():
    with open("redditPassword.txt", "r") as pass_file:
        # Read each line from the file, splitting on newline
        lines = pass_file.read().splitlines()
    # Close the file and return the list of lines
    pass_file.close()
    return lines

def authenticate():
    # Call the get pass function to open the file and extract the credentials
    lines = get_pass()
    
    # User password
    password = lines[0]
    
    # Client ID
    public_id = lines[1]
    
    # Authentication Key
    private_key = lines[2]

    # Request Temp ClientID
    client_auth = requests.auth.HTTPBasicAuth(public_id, private_key)

    # Dictionary to hold authentication
    post_data = {"grant_type": "password", "username": "TextualDatabase", "password": password}

    # This will be who is requesting API access
    headers = {"User-Agent": "TextualDatabase/0.1"}

    # Request access
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

    # Store access token
    TOKEN = response.json()["access_token"]

    # Add authorization to the headers
    headers["Authorization"] = f"bearer {TOKEN}"
    return headers

# Format time into mm-dd-yyyy H:M:S
def format_time(epoch_time):
    #Takes time in epoch format and converts to human readable in local time
    human_time = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime(epoch_time))
    return human_time

# Get data from reddit location
def get_data(headers, comment_preference, subreddit): 
    request_content = requests.get("https://oauth.reddit.com/" + subreddit, headers=headers, params={"limit" : "100"}).json()
 
    #Pandas dataframe to hold data
    subreddit_content = pd.DataFrame()

    # =====================================================================================================
    # GET DATABASE, MUST BE DONE INSIDE EACH THREAD | MONGODB CLIENT CANNOT BE CONVERTED INTO LOCKED OBJECT
    # =====================================================================================================

    # Get client
    client = get_client()

    # Get the specific database
    db = get_database(client)

    # Get the specific collection
    collection = db.RedditPosts

    # Initial post id
    post_after = 0
    i = 0
    while post_after != None:
        # Iterate through each post grabbed
        for post in request_content["data"]["children"]:
            
            # Get post id, post fullname, and subreddit title + post id
            post_id = post["data"]["id"]
            post_type_id = post["kind"] + "_" + post["data"]["id"]
            subreddit_header = "r/" + post["data"]["subreddit"] + "/comments/" + post_id
            
            # Print current post and iteration
            print("Thread: " + str(mp.current_process()) + ": Iteration: " + str(i) + " | " + subreddit_header)

            # Check if current post is the last in the subreddit
            post_after = request_content["data"]["after"]
            
            # |                                GET POSTS                                 |
            # |--------------------------------------------------------------------------|
            # |Go through each post and add its data                                     |
            # |Subbreddit: Name of the subreddit the post was obtained from              |
            # |Title: Title of the current post                                          |
            # |Post_ID: Unique identifier to find the post within the subreddit          |
            # |Selftext: Text body of the post                                           |
            # |Created_UTC: Time and date of the post's creation                         |
            # |Link: The to the specific post                                            |
            # |Upvotes: How many upvotes the post has                                    |
            # |Downvotes: How many downvotes the post has                                |
            # |--------------------------------------------------------------------------|
            subreddit_content = subreddit_content.append({
                "subreddit" : post["data"]["subreddit"],
                "title" : post["data"]["title"],
                "author" : post["data"]["author"],
                "post_id" : post_type_id,
                "selftext" : post["data"]["selftext"],
                "created_utc" : format_time(post["data"]["created_utc"]),
                "link" : "https://www.reddit.com/" + post["data"]["permalink"],
                "upvotes" : post["data"]["ups"],
                "downvotes" : post["data"]["downs"]},
                ignore_index=True) 

            # Rather than saving as a json file, get the data frame in dict format
            dict_dataframe = convert_to_dict(subreddit_content)

            # Add dict file to collection
            collection.insert_one(dict_dataframe)

            # Increment iteration
            i += 1

            # Get the comments for the current post
            # Calls a separate get request using the parent id of the current post
            # Pass the parent's database connection
            get_comments(subreddit_header, comment_preference, subreddit_content["post_id"][0], db) 
        
            # Clear dataframe
            subreddit_content = subreddit_content[0:0]

        # Get post after the current last from the previous fetch
        # The maximum allowed number of post per fetch is 100
        # By getting the id of the last post in that current iteration and searching for the next 100 post after it we can all the post from the subreddit
        # We keep doing this until there are no more post after
        request_content = requests.get("https://oauth.reddit.com/" + subreddit, headers=headers, params={"limit" : "100", "after" : post_type_id}).json()
         
# Get comments given a post id
def get_comments(post, comment_preference, post_id, database):

    # Request comments from specific post: limit max number of comments taken, depth max steps through comment tree
    request_comments = requests.get("https://oauth.reddit.com/" + post, headers=headers, params={"limit" : "500", "depth" : "5"}).json()
    
    # Pandas dataframe to hold data
    post_comments = pd.DataFrame()

    # Flag used to print comments only if found
    comment_found = False

    # Get RedditComment collection
    collection = database.RedditComments

    #Iterate though each comment and add its datat to a dataframe
    for comment in request_comments[1]["data"]["children"]:
       
        # Try to get comments from post, if they dont exist, throw error
        # (Some post may not have any comments)

        # |                                 GET COMMENTS                                 |
        # |------------------------------------------------------------------------------|
        # |Subbreddit: Name of the subreddit the post was obtained from                  |
        # |Author: Author of the comment (if available)                                  |
        # |Comment_ID: Unique identifier to find the post within the subreddit           |
        # |Body: Text body of the comment                                                |
        # |Created_UTC: Time and date of the comment's creation                          |
        # |Link: The to the specific comment                                             |
        # |Upvotes: How many upvotes the comment has                                     |
        # |Downvotes: How many downvotes the comment has                                 |
        # |Parent_Post: ID of the post this comment was made under                       |
        # |------------------------------------------------------------------------------|
        try:
            post_comments = post_comments.append({
                "subreddit" : comment["data"]["subreddit"],
                "author" : comment["data"]["author"],
                "comment_id" : comment["kind"] + "_" + comment["data"]["id"],
                "body" : comment["data"]["body"],
                "created_utc" : format_time(comment["data"]["created_utc"]),
                "link" : "https://www.reddit.com/" + comment["data"]["permalink"],
                "upvotes" : comment["data"]["ups"],
                "downvotes" : comment["data"]["downs"],
                "parent_post_id" : post_id},
                ignore_index=True)
        except KeyError:
            # If there were no comments on that post, print an error
            print("Comment not found")
        else:
            comment_found = True
    
    # If a comment was found under the parent post, write it to the database
    if comment_found: 
            # Rather than saving as a json file, get the data frame in dict format
            dict_dataframe = convert_to_dict(post_comments)
            
            # Add dict file to collection
            collection.insert_one(dict_dataframe)       

    # Clear dataframe
    # post_comments = subreddit_content[0:0]

# Convert pandas dataframe to json and save as output file
def save_as_json(dataframe, file_name):
    dataframe.to_json(file_name + ".json", orient="index")

# Convert pandas dataframe to dict
def convert_to_dict(dataframe):
    # Convert to dict
    dict_file = dataframe.to_dict('dict')

    # Return dict
    return dict_file

# Convert pandas dataframe to csv and save as output file
def save_as_csv(dataframe, file_name):
    dataframe.to_csv(file_name + ".csv", sep="\n", encoding="utf-8")

# Main function, takes command line arguments for the subreddits to search, dedicate a thread for each if available
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please enter the name of a subreddit as a command line argument")
        sys.exit()

    # |------------ SAMPLE SUBREDDITS ------------|
    # | List of possbile subreddits to search:    |
    # | "r/Music/new",                            |
    # | "r/StarWars/new",                         | 
    # | "r/space/new",                            |
    # | "r/science/new",                          |
    # | "r/AskHistorians/new",                    |
    # | "r/cats/new",                             |
    # | "r/canada/new",                           |
    # | "r/nfl/new",                              |
    # | "r/formula1/new",                         |
    # | "r/Android/new",                          |
    # | "r/apple/new",                            |
    # | "r/programming/new"                       |
    # |-------------------------------------------|
    
    # Get credentials
    headers = authenticate()

    # Add users command line arguments to a list
    subreddit_list = []
    i = 1
    while i < len(sys.argv):
        subreddit_list.append(sys.argv[i])
        i += 1 

    # Prompt the user for their preference on comment saving format
    # For some reason (classic programming language weirdness) python does not have do while loops so it is emulated using break statements

    # Validate the user input
    while True:
        # Get user input
        separate_comments = input("Would you like comments saved individually or together? 0. Individual | 1. Together: ")
        
        # If the input is valid, break out
        if separate_comments == "0" or separate_comments == "1":
            break
        else:
            # Print error message if user input is not valid
            print("Invalid input, please input a value of either 0 or 1")

    # Make a partial function since using multiple parameters
    partial_get_data = functools.partial(get_data, headers, separate_comments) 
    pool=mp.Pool(mp.cpu_count())
    
    # Run the multiple threads on different subreddits
    results=pool.map(partial_get_data, subreddit_list)
    pool.close() 
