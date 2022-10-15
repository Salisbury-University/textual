"""
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
"""
import configTokens as con
import tweepy
import pandas as pd

def getTweets(client,search,iterate=1,results=100):
    tweetList = []
    for i in range(0,iterate,1):
        response = client.search_recent_tweets(query=search,expansions='author_id',tweet_fields='created_at',max_results=results)
    
        users = {u['id']: u for u in response.includes['users']}
        for info in response.data:
            tweetInfo = []
            if users[info.author_id]:
                user = users[info.author_id]            
                tweetInfo.append(user.username) # adds username to result
            tweetInfo.append(info.text) # add content of tweet to result
            tweetInfo.append(info.created_at) # add when tweeted to result
            
            # adds complete "tuple" of information
            tweetList.append(tweetInfo)

    data = pd.DataFrame(tweetList,columns=['User','Tweet','Date Tweeted'])
    return data

if __name__ == "__main__":
    client = tweepy.Client(bearer_token=con.BEARER_TOKEN) # gives us access to the api in the program

    # a list of queries to search for recent tweets
    queries = ['#covid19 lang:en -is:retweet -has:media',
                '#python lang:en -is:retweet -has:media',
                '#c++ lang:en -is:retweet -has:media',
                '#overwatch2 lang:en -is:retweet -has:media',
                '#eldenring lang:en -is:retweet -has:media',
                '#coding lang:en -is:retweet -has:media',
                '#rickandmorty lang:en -is:retweet -has:media',
                '#twitter lang:en -is:retweet -has:media',
                '#salisburyuniversity lang:en -is:retweet -has:media',
                '#metaquest lang:en -is:retweet -has:media',
                '#southpark lang:en -is:retweet -has:media',
                '#tiktoc lang:en -is:retweet -has:media',
                '#breastcancerawareness lang:en -is:retweet -has:media',
                '#iphone14 lang:en -is:retweet -has:media',
                '#election2022 lang:en -is:retweet -has:media']
    i = 1
    for query in queries:
        # create a file name for the csv file
        fileName = "tweets" + str(i) + ".csv"
        i+=1

        data = getTweets(client,query,iterate=10) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
