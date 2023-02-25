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

# Used to connect to the mongo DB
from pymongo import MongoClient

if __name__ == "__main__":
    print("Program end...")
