import requests
import json
import requests.auth
import sys

# Read in password from separate file
def get_pass():
    with open("redditPassword.txt", "r") as pass_file:
        lines = pass_file.read().splitlines()
    pass_file.close()
    return lines

def authenticate():
    lines = get_pass()
    
    # User password
    password = lines[0]
    
    # Client ID
    public_id = lines[1]
    
    # Authentication Key
    private_key = lines[2]

    # Request Temp ClientID
    client_auth = requests.auth.HTTPBasicAuth(public_id, private_key)

    # Dictionary to hold authentication
    post_data = {"grant_type": "password", "username": "TextualDatabase", "password": password}

    # This will be who is requesting API access
    headers = {"User-Agent": "TextualDatabase/0.1"}

    # Request access
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

    # Store access token
    TOKEN = response.json()["access_token"]

    # Add authorization to the headers
    headers["Authorization"] = f"bearer {TOKEN}"
    return headers

# Get data from reddit location
def get_data(headers): 
    request_content = requests.get("https://oauth.reddit.com/api/v1/" + "me", headers=headers).json()

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please enter the name of a subreddit as a command line argument")
        sys.exit()

    #print(sys.argv[1])
    headers = authenticate()
    get_data(headers)
