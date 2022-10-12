# Date: 10/6/2022
# Description: Use the Reddit API to collect content a specified subreddit and store as a .json or .csv file

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

# Read in password from separate file
def get_pass():
    with open("redditPassword.txt", "r") as pass_file:
        lines = pass_file.read().splitlines()
    pass_file.close()
    return lines

def authenticate():
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
def get_data(headers, subreddit): 
    request_content = requests.get("https://oauth.reddit.com/" + subreddit, headers=headers, params={"limit" : "100"}).json()

    #Pandas dataframe to hold data
    subreddit_content = pd.DataFrame()

    for post in request_content["data"]["children"]:
        post_id = post["data"]["id"]
        #request_comments = requests.get("https://oauth.reddit.com/" + subreddit + "/comments/" + post_id + "/", headers=headers, params={"limit" : "5"}).json()

        #print(request_comments)

        subreddit_content = subreddit_content.append({
            "subreddit" : post["data"]["subreddit"],
            "title" : post["data"]["title"],
            "selftext" : post["data"]["selftext"],
            "created_utc" : format_time(post["data"]["created_utc"]),
            "link" : "https://www.reddit.com/" + post["data"]["permalink"],
            "upvotes" : post["data"]["ups"],
            "downvotes" : post["data"]["downs"]},
            ignore_index=True)
    
    save_as_json(subreddit_content, subreddit_content["subreddit"][0])

# Convert pandas dataframe to json and save as output file
def save_as_json(dataframe, file_name):
    dataframe.to_json(file_name + ".json", orient="index")

# Convert pandas dataframe to csv and save as output file
def save_as_csv(dataframe, file_name):
    dataframe.to_csv(file_name + ".csv", sep="\n", encoding="utf-8")

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please enter the name of a subreddit as a command line argument")
        sys.exit()

    subreddit_list = ["r/Music/hot", "r/StarWars/hot", "r/space/hot", "r/science/hot", "r/AskHistorians/hot", "r/cats/hot", "r/canada/hot", "r/nfl/hot", "r/formula1/hot", "r/Android/hot", "r/apple/hot", "r/programming/hot"]
    headers = authenticate()

    #items = ((headers, subreddit) for subreddit in subreddit_list)
    #print(items)
    
    # Make a partial function since using multiple parameters
    partial_get_data = functools.partial(get_data, headers) 
    pool=mp.Pool(mp.cpu_count())
    
    #results=itertools.starmap(get_data, items)
    results=pool.map(partial_get_data, subreddit_list)
    pool.close()

    print(sys.argv[1])
    #get_data(headers, sys.argv[1])
