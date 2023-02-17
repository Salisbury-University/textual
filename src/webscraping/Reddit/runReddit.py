import pymongo as db
import sys
from time import sleep
import os

# run loop continuously
"""
I added some error catching just for a clear place where it failed or was interrupted by the user.
"""
while True:
    try:
        try:
            fd=open("subreddit.txt","r")
            sub_reddits=""
            next_line=fd.readline()
            while next_line!="":
                sub_reddits+=next_line[:-1]
                next_line=fd.readline()
                if next_line=="":
                    sub_reddits+="w "
                else:
                    sub_reddits+=" "
            os.system("python3.7 readRedditDB" + sub_reddits)
        except:
            print("\nProgram Failed")
            sys.exit()
        print(sub_reddits)
        sleep(20) # this sleep  makes sure it is only run every day
    except:
        print("\nScraper Terminated")
        sys.exit()