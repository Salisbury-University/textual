### Read Reddit

# Purpose:
<br/>
Collect post and their respective comments and save them under .json files.
<br/>
Allow the user to select which subreddits they would like to extract content from.
<br/>
Uses multithreading to save time when processing multiple subreddits.
<br/>

# Operation:
<br/>
Pass the names of the desired subreddits in the following format: "r/subreddit/sortby".
<br/>
Sort by type may be left blank or use a specifier such as hot, new, top, etc...
<br/>
Output of each subreddit will be saved into two separate file categories, the first will contain all the post from the subreddit. The second will contain all the comments for a given post. The comments will be stored in a file with a name containing the parent post id.
<br/>
