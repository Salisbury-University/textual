# YoutubeComments.py:


## Purpose of this program: 
  This program scrapes YouTube comments and then inserts them into the database along with metadata describing the comment itself and the video it was posted under.


# Algorithm:

  * Uses YouTube API to Request every available YouTube video category in the US region.
  * Uses a multiprocessing pool with the YouTube API to request up to 100 videos from every video category in parallel.
  * Each process in the pool is assigned a different video category.
  * After each process in the pool finishes getting the videos for its assigned category, it will request up to 100 of the most recent comments and up to 100 of the most relevant comments for each video it received.
  * This results in up to 100 videos retrieved and up to 20,000 comments retrieved per available video category.
  * Each process will try to insert all the metadata it retrieved into the database.
  * Before the Program terminates, It prints the results of its execution.



# Things to know:
  * Link to Youtube API V3 Documentation: https://developers.google.com/youtube/v3/docs
  * You can change the number of requested comments and videos by changing the constants NUMBER_OF_COMMENTS and NUMBER_OF_VIDEOS
  If the assigned video category chart is not available, the process will be given a new category to request videos from.
  * The program will not insert comments that are already in the database.
  * The program will not insert shorts or videos that do not have any comments, have comments disabled.
  * Our project can make up to 10,000 requests to the Youtube API every day.
