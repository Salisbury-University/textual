# -*- coding: utf-8 -*-



import googleapiclient._auth
import googleapiclient.discovery
import googleapiclient.errors
from pymongo import MongoClient


def tag2str(taglist):
    str = ""
    for tag in taglist:
        str = str + ',' + tag
    return str

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
    
        try:
            print("requesting videos")
            response = request.execute()
            print("Successfully received videos for category:", category)
            items = response["items"]
            
            #store metadata about the 10 videos in this category
            videos = []
            for item in items:
                thisDict = {'vId': item['id'], 
                            "vidTitle": item['snippet']['title'],
                            "channelTitle": item['snippet']['channelTitle'],
                            "vidTags": item['snippet']['tags'], #store one string containing the tags
                            "commentCount": item['statistics']['commentCount']
                            }
                videos.append(thisDict)
            
            print("VIDEOS in LIST:", len(videos))

            # request 5 most recent commentThreads per video
            for video in videos:
                if video["commentCount"] != '0':
                    print("requesting comment threads")
                    request = youtube.commentThreads().list(
                    part="snippet",
                    order="time",
                    textFormat="plainText",
                    videoId=video['vId']
                    )

                    response = request.execute()
                    items = response['items']

                    #store metadata about the 5 comment threads
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
                    
                    print("COMMENTS in LIST:", len(commentThreads))
                    #store video info
                    print("Checking if video exists in db")
                    print("video collection find count:", video_collection.find({'vId': { "$in": video['vId']}}).count())

                    if video_collection.find({'vId': { "$in": video['vId']}}).count() > 0:
                        video_collection.insert_one(video)
                        print("inserting video", video)
                    else:
                        print("NOT inserting video", video)


                    #store comment info
                    for comment in commentThreads:
                        print("comment collection find count:", comment_collection.find({'cId': { "$in": comment['cId']}}).count())

                        print(comment_collection.find({'cId': { "$in": comment['cId']}}).count())
                        if comment_collection.find({'cId': { "$in": comment['cId']}}).count() > 0:
                            comment_collection.insert_one(comment)
                            print("inserting comment", comment)
                        else:
                            print("NOT inserting comment", comment)
            
                    
                

                        
                        
        except:
            print("most popular chart for category", category["title"]," is not supported or not available")
    
    close_database(client)
        
            
            
        

            



            
                        


            



    
    


    

