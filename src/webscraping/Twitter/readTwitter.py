import tweepy
import tweet.readtweet as tw
import multiprocessing as mp
import threading

if __name__ == "__main__":
    client = tweepy.Client(bearer_token=tw.BEARER_TOKEN) # gives us access to the api in the program
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
        data = tw.get_tweets(client,query,1000) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
        print("Done searching for those tweets.\n")

    print('Done.\nResults saved in *.csv files.\n')

    users = ['elonmusk','WHO','NASA']
    
    for user in users:
        userId = client.get_user(username=user)
        print('Grabbing Tweets from @{}...'.format(user))
        print('Tweets Received: {}'.format(tw.get_user_tweets(client,user,userId.data.id)))
        print('Finished grabbing tweets.\n')

    print('Done.\nTweets saved to *.csv files.')
