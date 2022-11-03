from pymongo import MongoClient

# get_credentials() -> gets the credentials from the info file 
# parameters -> text file containing username and password of database
# returns -> a list of the lines

def get_credentials(info_file): 
    
    # open file, read lines and split on newline
    with open(info_file, 'r') as pass_file: 
        lines = pass_file.read().splitlines()
    pass_file.close()

    return lines


# get_client() -> logs into the database and returns the client
# parameters -> text file containing the username and password for the database
# returns -> the client

def get_client(info_file):

    lines = get_credentials(info_file)
    
    username = lines[0]
    password = lines[1]

    client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

    return client

# get_database() -> returns textual database
# parameters -> the client object for the database
# returns -> our specific database

def get_database(client):

    return client.textual

# close_database() -> closes database
# parameters -> the client object for the data
# returns -> nothing

def close_database(client): 

    client.close()