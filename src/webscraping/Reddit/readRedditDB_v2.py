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
    client_id = credentials[0]
    client_secret = credentials[1]
    user_agent = credentials[2]
    user_id = credentials[3]
    user_password = credentials[4]

    reddit_api = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent, username = user_id, password = user_password)

    return reddit_api

if __name__ == "__main__":
    credentials = get_credentials()
    api_obj = api_connection(credentials)
    
    print(api_obj)

    print("Program end...")
