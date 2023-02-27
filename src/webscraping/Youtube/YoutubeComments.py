# YoutubeComments.py
# This program uses the YouTube API v3 to scrape comments from a large amount
# of YouTube videos. You can change the maximum number of comments that will
# be requested from the API by changing the value of these two variables: 
# 
# NUMBER_OF_VIDEOS
# NUMBER_OF_COMMENTS

import googleapiclient._auth
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import multiprocessing as mp
import functools
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Maximum number of videos requested 
NUMBER_OF_VIDEOS = 100

# Maximum number of Comments requested per video
NUMBER_OF_COMMENTS = 200

def initialize_lock(this_lock):
    # Initialize each process with a shared lock variable

    global lock # each process creates this global variable
    lock = this_lock # and assigns the shared lock to each process

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

    # Call the get credentials function to open the file and extract the credentials
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

def getDocumentCount():
    client = get_client()

    # Get a database from the connection
    database = get_database(client)

    # Get a collections
    video_collection = database.YoutubeVideo
    comment_collection = database.YoutubeComment
    
    # Get number of documents in both collections
    videoCount = video_collection.count_documents({})
    commentCount = comment_collection.count_documents({})
    
    #close database
    close_database(client)

    #return the number of documents in both collection
    return [videoCount, commentCount]

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
        maxResults=NUMBER_OF_VIDEOS,
        videoCategoryId = category['id']
        )
    
    try:
        response = request.execute() # Request 50 most popular videos from this category
        items = response["items"]

        #store metadata about the 25 videos in this category
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
                # print("'KeyERROR': This video has no comments available. Next video...")
                pass
    except HttpError:
            print("Thread " + str(mp.current_process().pid) + ":", "'HTTPError': most popular chart for category:", "'" + category["title"] + "'"," is not supported or not available")
            return []

    return videos
    
    
def getComments(youtube, video, sortBy):
    # Comment Request Parameters
    request = youtube.commentThreads().list(
    part="snippet",
    order=sortBy,
    textFormat="plainText",
    videoId=video['vId'],
    maxResults=(NUMBER_OF_COMMENTS/2),
    )

    try: # Try to get 50 comments from this video
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

    except HttpError: # Occurs when comments are disabled for this video
        print( "Thread " + str(mp.current_process().pid) + ":", "'HTTPError': This video has no comments available. Next video...")


def scrape_comments(youtube, category):

    with lock:
        print("Thread " + str(mp.current_process().pid) + ": Looking at Category: " + category["title"])
    # Get a connection to the server
    client = get_client()

    # Get a database from the connection
    database = get_database(client)

    # Get a collection from the database (YoutubeVideo, holds video metadata, YoutubeComment holds comment metadata)
    video_collection = database.YoutubeVideo
    comment_collection = database.YoutubeComment

    numVideosInserted = 0 
    numCommentsInserted = 0

    videos = getVideos(youtube, category) # request 50 most popular videos per category

    for video in videos:
        commentThreadsT = getComments(youtube, video, "time") # request 50 most recent commentThreads per video
        commentThreadsR = getComments(youtube, video, "relevance") # request 50 most relevent commentThreads per video

        #store video metadata
        if video_collection.count_documents({ 'vId': video["vId"] }, limit = 1) == 0: #check if this video is in the database
            video_collection.insert_one(video)
            numVideosInserted += 1
        else:
            #with lock:
                #print("Thread " + str(mp.current_process().pid) + ":", "video", video['vId'], "is already in database")
            pass

        if commentThreadsT != None: # if the list is not empty
            #store metadata of most recent comments
            for comment in commentThreadsT:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1
                except DuplicateKeyError: # two threads tried to insert the same comment at the same time.
                    #with lock:
                        #print("Thread " + str(mp.current_process().pid) + ":", "comment", comment['cId'], "is already in the database")
                    pass

        if commentThreadsR != None: # if the list is not empty
            #store metadata of most relevant comments
            for comment in commentThreadsR:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1

                except DuplicateKeyError:
                    #with lock:
                        #print("Thread " + str(mp.current_process().pid) + ":", "comment", comment['cId'], "is already in the database")
                    pass
    
    with lock:
        print()

    close_database(client)

    with lock:
        print("Thread " + str(mp.current_process().pid) + ": finished Category: " + category["title"] + "\ninserted", numCommentsInserted, "comments and", numVideosInserted,"videos\n")
    
    return [numVideosInserted, numCommentsInserted]

if __name__ == "__main__":
    
    api_service_name = "youtube"
    api_version = "v3"

    # Get API key and create an API client
    key = getKey()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

    categories = getCategories(youtube)

    # Create a Lock for the processes to share
    lock = mp.Lock()

    # get the initial number of documents before inserting more into the database 
    DocumentCount = getDocumentCount() 

    # Make a partial function since using multiple parameters
    partial_scrape_comments = functools.partial(scrape_comments, youtube,)
    pool=mp.Pool(mp.cpu_count(), initializer=initialize_lock, initargs=(lock,))

    # Run each process on a different category
    results=pool.map(partial_scrape_comments, categories,)
    pool.close()

    totalV = 0
    totalC = 0
    for total in results:
        totalV += total[0]
        totalC += total[1]
    
    print("                     <RESULTS>                           ")
    print("<-------------------------------------------------------->")

    print("Initial number of documents in YoutubeComment Collection: ", DocumentCount[0])
    print("Initial number of documents in YoutubeVideo Collection: ", DocumentCount[1])
    print()

    print("Total Videos inserted: ", totalV)
    print("Total Comments inserted: ", totalC)
    print()

    DocumentCount = getDocumentCount()

    print("Current number of documents in YoutubeComment Collection: ", DocumentCount[0])
    print("Current number of documents in YoutubeVideo Collection: ", DocumentCount[1])
