import tweepy
import tweet.readtweet as tw
import multiprocessing as mp
import threading

if __name__ == "__main__":
    print("Scraping Tweets...\n")
    i = 1
    client = tweepy.Client(bearer_token=tw.BEARER_TOKEN) # gives us access to the api in the program

    f = open("queries.md","r")
    queries=[]
    for text in f:
        queries.append(text)
    
    for query in queries:
        print("Searching for tweets that fit the query: {}".format(queries[i-1]),end='')
        # create a file name for the csv file
        fileName = "tweets" + str(i) + ".csv"
        i+=1 
        data = tw.getTweets(client,query,1000) # grabs the most recent tweets
        data.to_csv(fileName,index=False) # creates the csv file
        print("Done searching for those tweets.\n")

    print('Done.\nResults saved in *.csv files.')
    f.close()