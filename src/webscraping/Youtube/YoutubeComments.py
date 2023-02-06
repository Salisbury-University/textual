#YoutubeComments.py

import googleapiclient._auth
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import multiprocessing as mp
import functools
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def getKey():
    with open("YTkey.txt", 'r') as keyFile:
        text = keyFile.read()
    keyFile.close()
    return text

def get_credentials():
    with open("mongopassword.txt", "r") as pass_file:
        # Read each line from the file, splitting on newline
        lines = pass_file.read().splitlines()
    # Close the file and return the list of lines
    pass_file.close()
    return lines

# Connect to the database
def get_client():
    # Needs to be done this way, can't push credentials to github
    # Call the get pass function to open the file and extract the credentials
    lines = get_credentials()

    # Get the username from the file
    username = lines[0]

    # Get the password from the file
    password = lines[1]

    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

    # Return the client
    return client

# Get the database, we are using the textual database | hardcoded currently (bad)
def get_database(client):
    return client.textual

# Important, close the database
def close_database(client):
    # Close the connection to the database
    client.close()

def getCategories(youtube):
    #request a list of all youtube categories used in the US
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()
    
    # get all youtube categories used in the US (there's 32 categories)
    categories = []
    items = response["items"]
    for item in items:
        thisDict = {"id": item['id'], "title":item['snippet']['title'],}
        categories.append(thisDict)

    return categories

def getVideos(youtube, category):
    request = youtube.videos().list(
        part="id,snippet,statistics",
        chart="mostPopular",
        regionCode="US",
        maxResults=25,
        videoCategoryId = category['id']
        )
    #print("currently on category:", category['title'])
    try:
        #print("requesting videos")
        response = request.execute()
        #print("Successfully received videos for category:", category["title"])
        items = response["items"]

        #store metadata about the 10 videos in this category
        videos = []
        for item in items:
            try:
                #check if each video has comments
                if item["statistics"]["commentCount"] is not None and item["statistics"]["commentCount"] != '0':
                    thisDict = {'vId': item['id'], 
                                "vidTitle": item['snippet']['title'],
                                "channelTitle": item['snippet']['channelTitle'],
                                "commentCount": item['statistics']['commentCount'],
                                "category": category['title']
                                }
                    videos.append(thisDict)
            except KeyError:
                print("'KeyERROR': This video has no comments available. Next video...")
    except HttpError: 
            print("HTTPError: most popular chart for category:", "'" + category["title"] + "'"," is not supported or not available")
            return []

    return videos
    
    
def getComments(youtube, video, sortBy):
    # Comment Request Parameters
    request = youtube.commentThreads().list(
    part="snippet",
    order=sortBy,
    textFormat="plainText",
    videoId=video['vId'],
    maxResults=20,
    )

    try: # Try to get 20 comments from this video
        response = request.execute() #make the request
        items = response['items'] #results

        #store metadata about the 20 comment threads into a list of dictionaries
        commentThreads = []
        for item in items:
            thisDict = {
                "cId": item['snippet']['topLevelComment']['id'],
                "text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                "likeCount": item['snippet']['topLevelComment']['snippet']['likeCount'],
                "replyCount": item['snippet']['totalReplyCount'],
                "publishDate": item['snippet']['topLevelComment']['snippet']['publishedAt'],
                "lastUpdated": item['snippet']['topLevelComment']['snippet']['updatedAt'],
                "vId": video['vId']
            }
            commentThreads.append(thisDict)
            
        return commentThreads

    except HttpError: # Occurs when comments are disabled
        print("'HTTPERROR': This video has no comments available. Next video...")


def scrape_comments(youtube, category):

    print("Thread: " + str(mp.current_process().pid) + ": Looking at Category: " + category["title"])
    # Get a connection to the server
    client = get_client()

    # Get a database from the connection
    database = get_database(client)

    # Get a collection from the database (YoutubeVideo, holds video metadata, YoutubeComment holds comment metadata)
    video_collection = database.YoutubeVideo
    comment_collection = database.YoutubeComment

    numVideosInserted = 0 
    numCommentsInserted = 0

    videos = getVideos(youtube, category) # request 10 most popular videos per category

    for video in videos:
        commentThreadsT = getComments(youtube, video, "time") # request 20 most recent commentThreads per video
        commentThreadsR = getComments(youtube, video, "relevance") # request 20 most relevent commentThreads per video

        #store video metadata
        if video_collection.count_documents({ 'vId': video["vId"] }, limit = 1) == 0: #check if this video is in the database
            video_collection.insert_one(video)
            numVideosInserted += 1
        else:
            print("video", video['vId'], "is already in database")

        #store metadata of most recent comments
        for comment in commentThreadsT:
            # if comment_collection.count_documents({ 'cId': comment["cId"] }, limit = 1) == 0: #check if this comment is in the database
            try: # prevents a race condition between threads inserting the same comments
                comment_collection.insert_one(comment)
                numCommentsInserted += 1
            except DuplicateKeyError:
                print("comment", comment['cId'], "is already in the database")
            # else:
            #    print("comment", comment['cId'], "is already in database")

        #store metadata of most relevant comments
        for comment in commentThreadsR:
            # if comment_collection.count_documents({ 'cId': comment["cId"] }, limit = 1) == 0: #check if this comment is in the database
            try: # prevents a race condition between threads inserting the same comments
                comment_collection.insert_one(comment)
                numCommentsInserted += 1
            except DuplicateKeyError:
                print("comment", comment['cId'], "is already in the database")
            # else:
            #    print("comment", comment['cId'], "is already in database")

    print()

    close_database(client)

    print("Thread: " + str(mp.current_process().pid) + ": finished Category: " + category["title"] + "\ninserted", numCommentsInserted, "comments and", numVideosInserted,"videos\n")



if __name__ == "__main__":
    
    api_service_name = "youtube"
    api_version = "v3"
    
    # Get API key and create an API client
    key = getKey()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

    categories = getCategories(youtube)

    # Make a partial function since using multiple parameters
    partial_scrape_comments = functools.partial(scrape_comments, youtube)
    pool=mp.Pool(mp.cpu_count())

    # Run the multiple threads on different subreddits
    results=pool.map(partial_scrape_comments, categories,)
    pool.close()
