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
def get_user_tweets(client,user,result_limit=100):
    userId=client.get_user(username=user) # retrieves the userId for access to the tweets
    tweets = [] # list that will contain lists of tweet information from user

    # Twitter's API only allows for grabbing 100 unique tweets
    # Paginator helps to grab more in the function default is 100
    for response in tweepy.Paginator(client.get_users_tweets,id=userId.data.id,exclude=['retweets','replies'],
                                     tweet_fields=['created_at','public_metrics'],max_results=100)\
                                     .flatten(limit=result_limit):

        tupleList = [] # the list of the information of one tweet
        tupleList.append(response.text) # stores the content of the actual tweet
        tupleList.append(response.public_metrics['like_count']) # stores number of likes
        tupleList.append(response.public_metrics['retweet_count']) # stores number of retweets
        tupleList.append(response.created_at) # stores the time it was created
        tweets.append(tupleList) # adds single tweet information to the total accumulation of tweets

    # stores tweets into a DataFrame via pandas
    data = pd.DataFrame(tweets,columns=['Tweet','# of Likes','# of Retweets','Published'])
    return data
    
"""
Function gets the most recent tweets with a specific search query
       (See query formatting on twitter developer website)
"""
def get_recent_tweets(client,search,wanted_results=100):
    tweetList = [] # list that will contain lists of tweet information

    # Twitter's API only allows for grabbing 100 unique tweets
    # Paginator helps to grab more in the function default is 100
    for response in tweepy.Paginator(client.search_recent_tweets,query=search,
                                 expansions='author_id',tweet_fields=['created_at','public_metrics'],
                                 sort_order='relevancy',max_results=100).flatten(limit=wanted_results):
        tweetInfo = [] # the list of the information of one tweet
        tweetInfo.append(response.text) # stores the content of the actual tweet
        tweetInfo.append(response.public_metrics['like_count']) # stores number of likes
        tweetInfo.append(response.public_metrics['retweet_count']) # stores number of retweets
        tweetInfo.append(response.created_at) # stores the time it was created    
        tweetList.append(tweetInfo) # adds single tweet information to the total accumulation of tweets

    # stores tweets into a DataFrame via pandas
    data = pd.DataFrame(tweetList,columns=['Tweet','# of likes','# of retweets','Date Tweeted'])
    return data

"""
This function will grab archieved tweet instead of the most recent with a specified start and end time. 
                              (Requires academic research access)
                Unable to test however the function is here for when access is granted
"""
def get_archive_tweets(client,search,date_start,date_end,wanted_results=100):
    for response in tweepy.Paginator(client.search_all_tweets,query=search,end_time=date_end,
                                 start_time=date_start,expansions='author_id',tweet_fields=['created_at','public_metrics'],
                                 sort_order='relevancy',max_results=100).flatten(limit=wanted_results):
        tweetInfo = []
        tweetInfo.append(response.text) # add content of tweet to result
        tweetInfo.append(response.public_metrics['like_count']) # adds the like count
        tweetInfo.append(response.public_metrics['retweet_count']) # adds the retweet count
        tweetInfo.append(response.created_at) # add when tweeted to result   
        
        # adds complete "tuple" of information
        tweetList.append(tweetInfo)

    data = pd.DataFrame(tweetList,columns=['Tweet','# of likes','# of retweets','Date Tweeted'])
    return data

def start(info):
    client=info[0]
    queryList=info[1]
    userList=info[2]
    for query in queryList:
        print('Searching Query {}...\n'.format(query))
        get_recent_tweets(client, query,1000).to_csv(query+".csv",index=False)
    for user in userList:
        print('Searching Tweet by @{}...\n'.format(user))
        fileName = user + ".csv"
        get_user_tweets(client,user,1000).to_csv(fileName,index=False)

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
    users = ['CNN','FoxNews','ABC','CBSNews','NBCNews','nytimes','TIME','Independent','WSJ','CNBC']

    print('Available Processors: {}\n'.format(mp.cpu_count()))
    pool = mp.Pool(mp.cpu_count()) # creates a pool of threads and makes it efficient by using # of processors avaialable

    mod = len(queries)%mp.cpu_count()
    task_range = len(queries)//mp.cpu_count()
    queriesList=[]
    queryList=[]

    """Splits up the queries into cpu_count() divisions"""
    for i in range(0,task_range*mp.cpu_count()):
        queryList.append(queries[i])
        if (i+1) % task_range == 0:
            queriesList.append(queryList)
            queryList=[]
    if mod != 0:
        iterate = 0
        for i in range(task_range*mp.cpu_count(),len(queries)):
            queriesList[iterate].append(queries[i])
            iterate+=1

    mod = len(users)%mp.cpu_count()
    task_range = len(users)//mp.cpu_count()
    usersList=[]
    userList=[]

    """  Splits up the users into cpu_count() divisions  """
    for i in range(0,task_range*mp.cpu_count()):
        userList.append(users[i])
        if (i+1) % task_range == 0:
            usersList.append(userList)
            userList=[]
    if mod != 0:
        iterate = 0
        for i in range(task_range*mp.cpu_count(),len(users)):
            usersList[iterate].append(users[i])
            iterate+=1
    
    """  Combines all data into one single list containing the parameters for each 'thread'  """
    param_list =[]
    for i in range(0,mp.cpu_count()):
        param_list.append([client,queriesList[i],usersList[i]])

    pool.map(start, param_list)
    print('Finished.')
    pool.close()