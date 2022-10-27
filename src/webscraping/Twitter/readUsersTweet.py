import tweepy
import configTokens as con
import pandas as pd

def getUserTweets(client,username,userId,result_limit=1000):
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

if __name__ == "__main__":
    client = tweepy.Client(bearer_token=con.BEARER_TOKEN)
    users = ['elonmusk','WHO','NASA']
    
    for user in users:
        userId = client.get_user(username=user)
        print('Grabbing Tweets from @{}...'.format(user))
        print('Tweets Received: {}'.format(getUserTweets(client,user,userId.data.id)))
        print('Finished grabbing tweets.')

    print('Done.\nTweets saved to *.csv files.')
        