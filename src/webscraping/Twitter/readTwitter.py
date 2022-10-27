import tweepy
import configTokens as con
import multiprocessing as mp
import threading
import pandas as pd

def getTweets(client,search,wanted_results=100):
    tweetList = []
    for response in tweepy.Paginator(client.search_recent_tweets,query=search,
                                 expansions='author_id',tweet_fields=['created_at','public_metrics'],
                                 sort_order='relevancy',max_results=100).flatten(limit=wanted_results):
        tweetInfo = []
        tweetInfo.append(response.text) # add content of tweet to result
        tweetInfo.append(response.public_metrics['like_count']) # adds the like count
        tweetInfo.append(response.public_metrics['retweet_count']) # adds the retweet count
        tweetInfo.append(response.created_at) # add when tweeted to resul    
        
        # adds complete "tuple" of information
        tweetList.append(tweetInfo)

    print("Tweets Recieved: {}".format(len(tweetList)))
    data = pd.DataFrame(tweetList,columns=['Tweet','# of likes','# of retweets','Date Tweeted'])
    return data

if __name__ == "__main__":
    print("Scraping Tweets...\n")
    i = 1
    client = tweepy.Client(bearer_token=con.BEARER_TOKEN) # gives us access to the api in the program

    f = open("queries.md","r")
    queries=[]
    for text in f:
        queries.append(text)
    
    for query in queries:
        print("Searching for tweets that fit the query: {}".format(queries[i-1]),end='')
        # create a file name for the csv file
        fileName = "tweets" + str(i) + ".csv"
        i+=1 
        data = getTweets(client,query,1000) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
        print("Done searching for those tweets.\n")

    print('Done.\nResults saved in *.csv files.')
    f.close()