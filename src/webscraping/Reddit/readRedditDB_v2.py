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

def get_data(credentials, subreddit):
    api_obj = api_connection(credentials)
    praw_api = PushshiftAPI(praw=api_obj)
    
    #Pandas dataframe to hold data
    subreddit_content = pd.DataFrame()

    posts = praw_api.search_submissions(subreddit=subreddit, limit=None)

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
    
    index = 0
    for post in posts:
        subreddit_content = {"subreddit" : post["subreddit"], "title" : post["title"], "author" : post["author"], "post_id" : post["id"], "selftext" : post["selftext"], "created_utc" : post["created_utc"], "link" : post["url"], "score" : post["score"]}

        print(subreddit_content)
        print("===================================================================================================")

if __name__ == "__main__":
    credentials = get_credentials() 
    subreddit_list = ["formula1", "apple", "nfl", "space"]

    pool=mp.Pool(mp.cpu_count())
    partial_get_data = functools.partial(get_data, credentials)
    results=pool.map(partial_get_data, subreddit_list)
    pool.close()
 
    print("Script end...")
