import pymongo

# Get authoriazation from file
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
    client = pymongo.MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

    # Return the client
    return client

# Get the database, we are using the textual database | hardcoded currently (bad)
def get_database(client):
    return client.textual

# Important, close the database
def close_database(client):
    # Close the connection to the database
    client.close()

if __name__=="__main__":
    client=get_client()
    db = get_database(client)

    """
        This aggregate function is a fast way to collect certain data points within a collection
        the one below basically just finds all the 'non unique' videos form the YoutubeVideo collection
        and places then inside a dictionary like object
    """
    cur = db.YoutubeVideo.aggregate(
        [
            {"$group":{"_id":"$vId","unique_ids":{"$addToSet":"$_id"},"count":{"$sum":1}}},
            {"$match":{"count":{"$gte":2}}}
        ]
    )

    # actual grabbing of the unique id's of where those duplicates are stored and 
    # deletes them accordingly
    dup_ids =[]
    for data in cur:
        del data["unique_ids"][0]
        for data_id in data["unique_ids"]:
            dup_ids.append(data_id)
    count = db.YoutubeVideo.delete_many({"_id":{"$in":dup_ids}})
    print(count.deleted_count,"documents removed from YoutubeVideo.")
    
    cur = db.YoutubeComment.aggregate(
        [
            {"$group":{"_id":"$cId","unique_ids":{"$addToSet":"$_id"},"count":{"$sum":1}}},
            {"$match":{"count":{"$gte":2}}}
        ]
    )

    # actual grabbing of the unique id's of where those duplicates are stored and 
    # deletes them accordingly
    dup_ids =[]
    for data in cur:
        del data["unique_ids"][0]
        for data_id in data["unique_ids"]:
            dup_ids.append(data_id)
    count = db.YoutubeComment.delete_many({"_id":{"$in":dup_ids}})
    print(count.deleted_count,"documents removed from YoutubeComment.")
    close_database(client)
