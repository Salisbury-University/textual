# Project Name(s): English Contextual Baseline Database
# Program Name: readRedditDB_v2.py
# Date: 10/6/2022
# Description: Use the Reddit API (Most likely PRAW) to collect content a specified subreddit and store it directly in the database

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

import praw # Reddit API
from pmaw import PushshiftAPI

# Used to connect to the mongo DB
from pymongo import MongoClient

# Used for continuous scraping
import pytz
import schedule
import time
from datetime import datetime

# Global timezone
tz = pytz.timezone('America/New_York') # Set your desired timezone here

# Get authoriazation from file
def get_db_credentials():
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
    lines = get_db_credentials()

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


# Read in password store in file (file is used to avoid pushing credentials to GitHub.)
def get_credentials():
    with open("redditPassword.txt", "r") as credentials: # Open file containing credentials as read only
        # Read each line in and store in a list
        lines = credentials.read().splitlines()
    # Close the file and return the list
    credentials.close()
    return lines

def api_connection(credentials):
    # Connect to the Reddit API using the credentials read in from the authentication file
    reddit_api = praw.Reddit(client_id = credentials[0], client_secret = credentials[1], user_agent = credentials[2], username = credentials[3], password = credentials[4])

    # Return the authenticated API object
    return reddit_api

def get_data(praw_api, subreddit, api_obj): 
    print("Starting {}".format(subreddit))
    
    posts = praw_api.search_submissions(subreddit=subreddit, limit=None)

    pool=mp.Pool(mp.cpu_count())
    
    partial_posts = functools.partial(push_posts, api_obj) 

    # Split list of posts into sublists that can be passed into multiple threads
    index = 0
    split_posts = []
    sub_list = []
    for post in posts:
        sub_list.append(post)
        index += 1
        if index % 100 == 0:
            split_posts.append(sub_list)
            sub_list = []

    # Run the multiple threads on different subreddits
    results=pool.map(partial_posts, split_posts)
    pool.close() 

# Push comments to database
def push_posts(api_obj, posts):
    # Get client
    client = get_client()

    # Get the specific database
    db = get_database(client)
    
    # Get the specific collection
    post_collection = db.RedditPosts_v2
    comment_collection = db.RedditComments_v2

    #Pandas dataframe to hold data
    subreddit_content = pd.DataFrame()
    comment_content = pd.DataFrame()

    # |                                POST INFO                                 |
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
    # If the total amount of data in the database is less than 148 GB, push Reddit posts
    if (database.command("dbstats")["fsUsedSize"] < 148481273344): 
        count = 0
        comment_count = 0
        for post in posts:        
            if int(post['num_comments']) > 0:
                # Get all comments and push to DB
                id = post["id"]
                curr_post = api_obj.submission(id=id)

                # Get comments in list form
                try:
                    curr_post.comments.replace_more(limit=500)
                    comments = curr_post.comments.list()

                    # Iterate through the comments and add the to database
                    iteration = 0
                    for comment in comments:
                        print("Thread: " + str(mp.current_process()) +  " | Pushing comment {}".format(iteration))
                        comment_content = {"comment_id: " : str(comment.id), "parent_id" : str(comment.parent_id), "subreddit" : str(comment.subreddit), "text" : comment.body, "created_utc" : str(comment.created_utc)}
                        
                        try:
                            comment_collection.insert_one(comment_content)
                            comment_count += 1
                        except:
                            print("Comment insertion failed")
                        iteration += 1
                except:
                    print("Failed to push comments")

            subreddit_content = {"subreddit" : str(post["subreddit"]), "title" : str(post["title"]), "author" : str(post["author"]), "post_id" : str(post["id"]), "text" : str(post["selftext"]), "created_utc" : str(post["created_utc"]), "link" : str(post["url"]), "score" : str(post["score"])}
            count += 1

            # Add DataFrame file to collection
            try:
                post_collection.insert_one(subreddit_content)
            except:
                print("Post insertion failed.")
    else:
        print("Database full, posts will not be pushed.")

def start_push():
    lines = []
    with open("reddit_list.txt", "r") as reddit_file:
        # Read each line from the file, splitting on newline
        lines = reddit_file.read().splitlines()
    # Close the file and return the list of lines
    reddit_file.close()

    # Get credentials for the Reddit API
    credentials = get_credentials()

    api_obj = api_connection(credentials)
    praw_api = PushshiftAPI(praw=api_obj)

    for sub in lines:
        get_data(praw_api, sub, api_obj)

    # Get the current date and time
    now = datetime.now(tz)

    # Open the file in append mode and write the date and time to the end of the file
    with open("reddit_log.txt", "a") as file:
        file.write(f"The script finished running at {now}\n")

    # Close the file
    file.close()

if __name__ == "__main__": 
    # Check if the job is scheduled to run every 100 seconds
    # Continuous loop, job will be scheduled to run every Tuesday at 5:00 PM
    while True:
        print("waiting to run...")
        if (datetime.now(tz).weekday() == 1) and (datetime.now(tz).hour == 17) and (datetime.now(tz).minute < 5): 
            start_push()
        time.sleep(100)

    print("Script end...")
