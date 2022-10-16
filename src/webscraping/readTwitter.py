import tweepy
import configTokens as con
import multiprocessing as mp
import threading
import pandas as pd

def getTweets(client,search,iterate=1,results=100):
    tweetList = []
    for i in range(0,iterate,1):
        response = client.search_recent_tweets(query=search,expansions='author_id',tweet_fields=['created_at','public_metrics'],sort_order='relevancy',max_results=results)
    
        users = {u['id']: u for u in response.includes['users']}
        for info in response.data:
            tweetInfo = []
            if users[info.author_id]:
                user = users[info.author_id]            
                tweetInfo.append(user.username) # adds username to result
            tweetInfo.append(info.text) # add content of tweet to result
            tweetInfo.append(info.public_metrics['like_count'])
            tweetInfo.append(info.public_metrics['retweet_count'])
            tweetInfo.append(info.created_at) # add when tweeted to result
            
            # adds complete "tuple" of information
            tweetList.append(tweetInfo)

    data = pd.DataFrame(tweetList,columns=['User','Tweet','# of likes','# of retweets','Date Tweeted'])
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
        data = getTweets(client,query,results=10) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
        print("Done searching for those tweets.\n")

    print('Done.\nResults saved in *.csv files.')
    f.close()