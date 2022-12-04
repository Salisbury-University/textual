# -*- coding: utf-8 -*-

import googleapiclient._auth
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import sys
from pymongo import MongoClient

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

if __name__ == "__main__":

    api_service_name = "youtube"
    api_version = "v3"
    
    # Get a connection to the server
    client = get_client()
    print("got client")
    # Get a database from the connection
    database = get_database(client)
    print("got database")

    

    # Get a collection from the database (YoutubeVideo, holds video metadata, YoutubeComment holds comment metadata)
    video_collection = database.YoutubeVideo
    comment_collection = database.YoutubeComment

    # Get API key and create an API client
    key = getKey()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

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

    # request 10 most popular videos per category
    for category in categories:
        request = youtube.videos().list(
        part="id,snippet,statistics",
        chart="mostPopular",
        regionCode="US",
        maxResults=10,
        videoCategoryId = category['id']
        )
        print("currently on category:", category['title'])
        try:
            print("requesting videos")
            response = request.execute()
            print("Successfully received videos for category:", category["title"])
            items = response["items"]            

            #except HttpError:
            #    print("HTTPError: most popular chart for category:", "'" + category["title"] + "'"," is not supported or not available")
            #    print()

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
                    print()

            #print("num VIDEOS in LIST:", len(videos))
            # request 20 most recent commentThreads per video
            for video in videos:
                request = youtube.commentThreads().list(
                part="snippet",
                order="time",
                textFormat="plainText",
                videoId=video['vId'],
                maxResults=20,
                )

                response = request.execute()
                items = response['items']

                #store metadata about the 20 comment threads
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
                

                #store video info
                if video_collection.count_documents({ 'vId': video["vId"] }, limit = 1) == 0:
                    print("inserting a video:", video["vidTitle"])
                    #video_collection.insert_one(video)
                else:
                    print("video already in database")

                #store comment info
                for comment in commentThreads:
                    if comment_collection.count_documents({ 'cId': comment["cId"] }, limit = 1) == 0:
                        print("inserting a comment from video:", video["vidTitle"])
                        #comment_collection.insert_many(commentThreads)
                    else:
                        print("comment already in database")
                print()
                
        except HttpError:
            print("HTTPError: most popular chart for category:", "'" + category["title"] + "'"," is not supported or not available")
            print()
        print()

    close_database(client)
