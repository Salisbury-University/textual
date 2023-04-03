# <---------------------------SUMMARY--------------------------->
# YoutubeComments.py

# This program uses the YouTube API v3 to scrape comments from a large amount
# of YouTube videos. You can change the maximum number of comments that will
# be requested from the API by changing the value of these two variables: 
# 
# NUMBER_OF_VIDEOS
# NUMBER_OF_COMMENTS
# 
# After running this program, up to <NUMBER_OF_VIDEOS> videos and up to
# <NUMBER_OF_COMMENTS> comments will be added to the database for each video topic and category.
# The videos will be stored in YoutubeVideo collection and the comments will be stored
# in YoutubeComment collection in the textual Database.
# <------------------------------------------------------------->

import googleapiclient._auth
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import multiprocessing as mp
import functools
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Maximum number of videos requested from each category
NUMBER_OF_VIDEOS = 50

# Maximum number of Comments requested per video
NUMBER_OF_COMMENTS = 200

# Number of searches done.
NUMBER_OF_SEARCHES = 30

# <--------------------------------------------------------------------->
# This function is called to initialize a lock to synchronize each process's
# print statements.
# <--------------------------------------------------------------------->
def initialize_lock(this_lock):

    global lock # each process creates this global variable
    lock = this_lock # and assigns the shared lock to each process

# <--------------------------------------------------------------------->
# This function reads in the API key from the text file. It is read from
# the file for security reasons.
# <--------------------------------------------------------------------->
def getKey():
    with open("YTkey.txt", 'r') as keyFile:
        text = keyFile.read()
    keyFile.close()
    return text

# <--------------------------------------------------------------------->
# This function reads in the mongodb credentials from a text file. It is
# read from the file for security reasons.
# <--------------------------------------------------------------------->
def get_credentials():
    with open("mongopassword.txt", "r") as pass_file:
        # Read each line from the file, splitting on newline
        lines = pass_file.read().splitlines()
    # Close the file and return the list of lines
    pass_file.close()
    return lines
# <--------------------------------------------------------------------->
# This function allows the program to connect to the database and returns
# a the MongoClient object used to access the database.
# <--------------------------------------------------------------------->
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

# <--------------------------------------------------------------------->
# Get the database, we are using the textual database
# hardcoded currently (bad)
# <--------------------------------------------------------------------->
def get_database(client):
    return client.textual

# <--------------------------------------------------------------------->
# This function closes the connection to the database.
# <--------------------------------------------------------------------->
def close_database(client):
    # Close the connection to the database
    client.close()

# <--------------------------------------------------------------------->
# Connects to the database and gets the number of documents in the
# YoutubeComment collection and the YoutubeComment collection. Returns a
# list of 2 integers. 
# list[0] = number of videos
# list[1] = number of comments
# <--------------------------------------------------------------------->
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

# <--------------------------------------------------------------------->
# Returns a list of Youtube Video Categories used in the US Region
# <--------------------------------------------------------------------->
def getCategories(youtube):
    #request a list of all youtube categories used in the US
    try:
        request = youtube.videoCategories().list(
            part="snippet",
            regionCode="US"
        )
        response = request.execute()
    except HttpError as error:
        # print ("An HTTP error", error.resp.status ," occurred:\n", error.content)
        exit()
        
    # get all youtube categories used in the US (there's 32 categories)
    categories = []
    items = response["items"]
    for item in items:
        thisDict = {"id": item['id'], "title":item['snippet']['title'],}
        categories.append(thisDict)

    return categories

# <--------------------------------------------------------------------->
# Uses the YouTube API and one category to return a list of Videos that 
# have been posted under that category.
# <--------------------------------------------------------------------->
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
    except HttpError as error:
            # print("Thread " + str(mp.current_process().pid) + ":", "'HTTPError': most popular chart for category:", "'" + category["title"] + "'"," is not supported or not available")
            return []

    return videos
    
# <--------------------------------------------------------------------->
# Using the Youtube API and Youtube video, requests a list of YouTube 
# comments. Depending on the value of "sortBy," this function returns 
# either a list of the most recent or most relevant comments under that
# video.
#  
# sortBy = "time" : most recent
# sortBy = "relevance" : most relevant
# <--------------------------------------------------------------------->
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

    except HttpError as error: # Occurs when comments are disabled for this video or if the request limit has been reached for YouTube API.
            pass
            # print ("An HTTP error", error.resp.status ," occurred:\n", error.content)
            #print( "Thread " + str(mp.current_process().pid) + ":", "'HTTPError': This video has no comments available.",)
            

# <--------------------------------------------------------------------->
# Each process in the multiprocessing pool runs this function in parallel
# with each process being given a different YouTube category. Once this 
# process finishes with their category, they are assigned a new category
# to scrape comments from. 
# <--------------------------------------------------------------------->

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
        try: # try except if this video is already in the database
            video_collection.insert_one(video)
            numVideosInserted += 1
        except: # continue with the next video
            pass

        if commentThreadsT != None: # if the list is not empty
            #store metadata of most recent comments
            for comment in commentThreadsT:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1
                except DuplicateKeyError: # two threads tried to insert the same comment at the same time.
                    pass

        if commentThreadsR != None: # if the list is not empty
            #store metadata of most relevant comments
            for comment in commentThreadsR:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1

                except DuplicateKeyError:
                    pass
    with lock:
        print()

    close_database(client)

    with lock:
        print("Thread " + str(mp.current_process().pid) + ": finished Category: " + category["title"] + "\ninserted", numCommentsInserted, "comments and", numVideosInserted,"videos\n")
    
    return [numVideosInserted, numCommentsInserted]

# <--------------------------------------------------------------------->
# This function makes use of a file named "YoutubeSearch.txt" to return a
# list of search topics to use as an argument for the API request. Since
# there is a limit to the number of requests that can be made per day, the
# full list of search topics are not all read in at once. Instead, the first
# <NUMBER_OF_SEARCHES> topics to appear after the placeholder are read and 
# stored into a list. The program then leaves a placeholder ("*") in the 
# text file to remember the last topic it searched for and will then begin 
# searching from that point in the text file the next time the program is run.
# <--------------------------------------------------------------------->

def getSearchTopics():
    searchTopics = []
    newFileLines = []
    placeholderFound = False
    with open("YoutubeSearch.txt", 'r+') as file:
        
        for index, line in enumerate(file):

            if '*' not in line:
                if len(searchTopics) < NUMBER_OF_SEARCHES and placeholderFound:
                    searchTopics.append(line.replace("\n", ""))

            else:
                placeholderFound = True
                newStarIndex = index + NUMBER_OF_SEARCHES
                continue

            newFileLines.append(line)
        
        if newStarIndex >= index:
            newStarIndex = newStarIndex - index

        newFileLines.insert(newStarIndex, "*\n")

        if len(newFileLines) > 0:
            file.seek(0)
            for line in newFileLines:
                file.write(line)

    return searchTopics

# <--------------------------------------------------------------------->
# This Function takes the youtube API object, the search result dictionary,
# and the list of categories as input. It uses the API to request the metadata 
# of the youtube video that corresponds to the given search result. it uses the
# category list to determine what category this video belongs to based on the
# video's category ID.
# <--------------------------------------------------------------------->
def searchToVideo(youtube, searchResult, categories):
    thisId = searchResult["id"]["videoId"]
    
    #request this specific video with this id
    request = youtube.videos().list(
        part="id,snippet,statistics",
        id = thisId,
        )
    try:
        response = request.execute()
    except HttpError as error:
        # print ("An HTTP error", error.resp.status ," occurred:\n", error.content)
        exit()
    items = response["items"]
    
    # get this video's category id
    for item in items:
        vidCategoryId = item["snippet"]["categoryId"]

    # get the video's category title
    for category in categories:
        if category["id"] == vidCategoryId:
            thisCategory = category["title"]

    for item in items:
        try:
            thisVideo = {'vId': item['id'], 
                        "vidTitle": item['snippet']['title'], 
                        "channelTitle": item['snippet']['channelTitle'], 
                        "commentCount": item['statistics']['commentCount'], 
                        "category": thisCategory}
            
        except KeyError: # Occurs when comments are disabled for this video
            # print( "Thread " + str(mp.current_process().pid) + ":", "'KeyError': This video has no comments available. Next video...")
            thisVideo = "noComments"

    # print("This Video = ", thisVideo)
    
    return thisVideo

# <--------------------------------------------------------------------->
# This function takes the youtube api, a list of categories, and one topic.
# The API is used to request 50 videos from a single topic. Then it gets
# data from the search results and stores them into a video dictionary.
# Each dictionary is stored into a list and the function returns a list 
# of video dictionaries.
# <--------------------------------------------------------------------->
def searchVideos(youtube, categories, topic):
    request = youtube.search().list(
        part="snippet",
        maxResults=50, # 50 is the highest integar accepted as a parameter
        q=topic,
        relevanceLanguage="en",
        type="video"
    )
    try:
        response = request.execute() # Request 50 most relevant videos using this keyword
    except HttpError as error:
        # print ("An HTTP error", error.resp.status ," occurred:\n", error.content)
        exit()
    items = response["items"]

    #store metadata about the 50 videos in this category
    videos = []
    for searchResult in items:
        thisVideo = searchToVideo(youtube, searchResult, categories)

        # if there are no comments for this video then ignore it.
        if thisVideo == "noComments":
            # print("This Video (with no comments) = ", thisVideo)                         
            continue # move on
        else:
            videos.append(thisVideo)

    return videos

# <--------------------------------------------------------------------->
# Each process in the multiprocessing pool runs this function in parallel
# with each process being given a different search topic. Once this 
# process finishes with their topic, they are assigned a new topic
# to scrape comments from. 
# <--------------------------------------------------------------------->
def scrape_comments_by_search(youtube, categories, topic):

    with lock:
        print("Thread " + str(mp.current_process().pid) + ": Searching for videos with relevance to: " + topic)
    
    # Get a connection to the server
    client = get_client()

    # Get a database from the connection
    database = get_database(client)

    # Get a collection from the database (YoutubeVideo, holds video metadata, YoutubeComment holds comment metadata)
    video_collection = database.YoutubeVideo
    comment_collection = database.YoutubeComment

    numVideosInserted = 0 
    numCommentsInserted = 0

    videos = searchVideos(youtube, categories, topic) # request 50 most popular videos per category

    for video in videos:
        commentThreadsT = getComments(youtube, video, "time") # request 50 most recent commentThreads per video
        commentThreadsR = getComments(youtube, video, "relevance") # request 50 most relevent commentThreads per video

        #store video metadata
        try: # try except if this video is already in the database
            video_collection.insert_one(video)
            numVideosInserted += 1
        except: # continue with the next video
            continue

        if commentThreadsT != None: # if the list is not empty
            #store metadata of most recent comments
            for comment in commentThreadsT:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1

                except DuplicateKeyError: # two threads tried to insert the same comment at the same time.
                    pass

        if commentThreadsR != None: # if the list is not empty
            #store metadata of most relevant comments
            for comment in commentThreadsR:
                # prevents a race condition between threads inserting the same comments
                try:
                    comment_collection.insert_one(comment)
                    numCommentsInserted += 1

                except DuplicateKeyError:
                    pass
    with lock:
        print()

    close_database(client)

    with lock:
        print("Thread " + str(mp.current_process().pid) + ": finished Topic: " + topic + "\ninserted", numCommentsInserted, "comments and", numVideosInserted,"videos\n")
    
    return [numVideosInserted, numCommentsInserted]


# <--------------------------------------------------------------------->
# Main Function
# <--------------------------------------------------------------------->
if __name__ == "__main__":
    
    api_service_name = "youtube"
    api_version = "v3"

    # Get API key and create an API client
    key = getKey()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

    # Get a list of YouTube video categories using YouTube API
    categories = getCategories(youtube)
    
    # Create a Lock for the processes to share
    lock = mp.Lock()

    # get the initial number of documents before inserting more into the database 
    DocumentCount = getDocumentCount() 
    
    getMostPopular = False

    if getMostPopular == True:
        print("     Scraping Comments from Most Popular Video Charts>")
        print("<-------------------------------------------------------->")
        # Make a partial function since using multiple parameters
        partial_scrape_comments = functools.partial(scrape_comments, youtube,)
        pool=mp.Pool(mp.cpu_count(), initializer=initialize_lock, initargs=(lock,))

        # Map each process to scrape comments from a different category in the list
        results=pool.map(partial_scrape_comments, categories,)
        pool.close()

        # counts the total number of videos and comments inserted by each process.
        totalV = 0
        totalC = 0
        for total in results:
            totalV += total[0]
            totalC += total[1]

    # get a list of Search topics from a txt file.
    topics = getSearchTopics()

    print("     Scraping Comments from Search Queries>")
    print("<-------------------------------------------------------->")
    # Make a partial function since using multiple parameters
    partial_scrape_comments_by_search = functools.partial(scrape_comments_by_search, youtube, categories,)
    pool=mp.Pool(mp.cpu_count(), initializer=initialize_lock, initargs=(lock,))

    # Map each process to scrape comments from each search topic in the list
    results=pool.map(partial_scrape_comments_by_search, topics,)
    pool.close()

    # add the total number of videos and comments scraped by search 
    for total in results:
        totalV += total[0]
        totalC += total[1]
    
    print("                     <RESULTS>                           ")
    print("<-------------------------------------------------------->")

    print("Initial number of documents in YoutubeVideo Collection: ", DocumentCount[0])
    print("Initial number of documents in YoutubeComment Collection: ", DocumentCount[1])
    print()

    print("Total Videos inserted: ", totalV)
    print("Total Comments inserted: ", totalC)
    print()

    DocumentCount = getDocumentCount()

    print("Current number of documents in YoutubeVideo Collection: ", DocumentCount[0])
    print("Current number of documents in YoutubeComment Collection: ", DocumentCount[1])
