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
            # runs the reddit scraper
            os.system("./run_yelp.sh")
        except:
            print("\nProgram Failed")
            sys.exit()
        sleep(20) # this sleep  makes sure it is only run every day
    except:
        print("\nScraper Terminated")
        sys.exit()
