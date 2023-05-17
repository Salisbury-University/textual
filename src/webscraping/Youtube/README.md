# YoutubeComments.py:


## Purpose of this program: 
  This program scrapes YouTube comments and then inserts them into the database along with metadata describing the comment itself and the video it was posted under.

# Algorithm:
  1. First the program checks to see if it should scrape from the most popular video categories by checking and updating a txt file. (Should only scrape using categories once every 7 days). This saves time and API requests.
  2. If, a week has not passed yet, skip to step 9.
  3. Otherwise the program uses YouTube API v3 to request 50 videos from every available YouTube Video Category in the US region.
  4. Uses a multiprocessing pool with the YouTube API to request up to 50 videos from every video category in parallel.
  5. Each process in the pool is assigned a different video category.
  6. After each process in the pool finishes getting the videos for its assigned category, it will request up to 100 of the most recent comments and up to 100 of the most relevant comments for each video it received.
  8. Each process will try to insert all the comments and metadata it retrieved into the database.
  9. By using a list of search topics read from another txt file, the program requests up to 50 videos that match each search query. (ex: Politics, Sports, Gaming)
  10. Uses a multiprocessing pool with the YouTube API to request up to 50 videos matching each search topic in parallel.
  11. each process is in the pool assigned a different search topic
  12. After each process in the pool finishes getting the videos for its assigned search topic, it will request up to 100 of the most recent comments and up to 100 of the most relevant comments for each video it received.
  13. Each process will try to insert all the comments and metadata it retrieved into the database.
  14. Before the program terminates, it prints the results of its execution.



# Things to know about the program:
  * Be sure to reference Youtube API v3 Documentation: https://developers.google.com/youtube/v3/docs
  * Our project has a quota of up to 10,000 requests to the Youtube API every day.
  * You can change the number of requested comments and videos per category/search topic by changing the constants NUMBER_OF_COMMENTS (Currently set to 200) and NUMBER_OF_VIDEOS (Currently set to 50).
  * You can change the number of search topics that the scraper will read from the txt file. (Currently set to 30)
  * When scraping using video categories, if the assigned video category chart is not available, the process will be given a new category to request videos from.
  * When scraping using search topics, each search costs 100 requests which can quickly exhaust the daily quota of requests and cause errors in the program. To make sure this doesn't happen, make sure that NUMBER_OF_SEARCHES <= 30.
  * The program will attempt to ignore duplicates that are already in the database. (It is possible that this may fail sometimes)
  * The program will not insert videos that are shorts, have 0 comments, or have comments disabled into the database.
  * There are commented out print statements that can be used for checking what is producing errors. They may prove useful for debugging.

