import tweepy
import multiprocessing as mp
import threading
import pandas as pd

# contains all needed tokens
API_KEY = 'IFEDLBv8T9jIXGIS0ZGai4c3p'
API_SECRET = 'prZxsgrfBrgyw9OiHV0kaD7QbQb59zGpeGTdgj5Y0m0u87HJzW'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAANNCiAEAAAAA50r8jFMy9%2FUsaj6S62w%2BzNCIYJA%3DNwwhlm170ZSPUagfM8lmqiLoF42ze18zD3KsOvzNqmFXyc9dEu'
ACCESS_TOKEN = '1579907913132306432-EaTkWeT5UdHqdNz009qRLHmrxNDhsi'
ACCESS_TOKEN_SECRET = 'KRMxRSOFRkpHirI4PYEYOvZ8LfqovDxaX1ZpyinsQhuob'
CLIENT_ID = 'SFk2UlN4RlgxU3BlRVVFdVNNelM6MTpjaQ'
CLIENT_SECRET = 'rC6BrlAUbhZE6aDl9JSzDEzOe0IlZiL6LbU9OftOQ8xhg8rgan'

"""
Function grabs the most recent tweets from a certain user with a specificed user ID
(Twitter assigns a unique ID to every user and we can access their recent tweets)
"""
def get_user_tweets(client,username,userId,result_limit=1000):
    fileName = username + ".csv"
    tweets = []
    for response in tweepy.Paginator(client.get_users_tweets,id=userId,exclude=['retweets','replies'],
                                     tweet_fields=['created_at','public_metrics'],max_results=100)\
                                     .flatten(limit=result_limit):
        tupleList = []
        tupleList.append(response.text)
        tupleList.append(response.public_metrics['like_count'])
        tupleList.append(response.public_metrics['retweet_count'])
        tupleList.append(response.created_at)
        tweets.append(tupleList)
    pd.DataFrame(tweets,columns=['Tweet','# of Likes','# of Retweets','Published']).to_csv(fileName,index=False)
    return len(tweets)

"""
Function gets the most recent tweets with a specific search query
       (See query formatting on twitter developer website)
"""
def get_tweets(client,search,wanted_results=100):
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

"""
This function will grab archieved tweet instead of the most recent with a specified start and end time. 
                             (Requires academic research access)
                                       (Coming Soon...)
"""
def get_archive_tweets(client,search,date_start,date_end,wanted_results=100):
    pass

"""
A function that will get comments of a specific tweet
                  (Coming Soon...)
"""
def __get_replies(client,tweet_id,wanted_results=100):
    pass


if __name__ == "__main__":
    client = tweepy.Client(bearer_token=BEARER_TOKEN) # gives us access to the api in the program
    queries = ['(death OR dead) lang:en -is:retweet -has:media -has:links',
        '"Functional Programming" (#python OR #scala OR #haskell) lang:en -is:retweet -has:media -has:links',
        '#c++ OR #c OR #csharp OR #java lang:en -is:retweet -has:media -has:links',
        '#overwatch2 lang:en -is:retweet -has:media -has:links',
        '"Salisbury University" lang:en -is:retweet -has:media -has:links',
        '"computer science" lang:en -is:retweet -has:media -has:links',
        '#rickandmorty lang:en -is:retweet -has:media -has:links',
        '#youtube lang:en -is:retweet -has:media -has:links',
        'college OR #collegelife lang:en -is:retweet -has:media -has:links',
        '"Virtual Reality" OR VR lang:en -is:retweet -has:media -has:links',
        '#southpark lang:en -is:retweet -has:media -has:links',
        'Netflix #DAHMER lang:en -is:retweet -has:media -has:links',
        'October (#halloween OR #breastcancerawareness) lang:en -is:retweet -has:media -has:links',
        '#midterms2022 lang:en -is:retweet -has:media -has:links',
        '#football OR #NFL lang:en -is:retweet -has:media -has:links']
    
    print("Scraping Tweets...\n")
    i = 1
    for query in queries:
        print("Searching for tweets that fit the query: {}\n".format(queries[i-1]),end='')
        # create a file name for the csv file
        fileName = "tweets" + str(i) + ".csv"
        i+=1 
        data = get_tweets(client,query,1000) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
        print("Done searching for those tweets.\n")

    print('Done.\nResults saved in *.csv files.\n')

    users = ['elonmusk','WHO','NASA']
    
    for user in users:
        userId = client.get_user(username=user)
        print('Grabbing Tweets from @{}...'.format(user))
        print('Tweets Received: {}'.format(get_user_tweets(client,user,userId.data.id)))
        print('Finished grabbing tweets.\n')

    print('Done.\nTweets saved to *.csv files.')
