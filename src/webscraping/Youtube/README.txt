<h1>YoutubeComments.py:</h1>

<p>
<b>Purpose of this program:</b><br> 
This program scrapes YouTube comments and then inserts them into the database along with metadata describing the comment itself and the video it was posted under.
</p>

<p>
<b>Algorithm:</b><br>
<ol>
<li>Uses YouTube API to Request every available YouTube video category in the US region.</li>
<li>Uses a multiprocessing pool with the YouTube API to request up to 100 videos from every video category in parallel.</li>
<li>Each process in the pool is assigned a different video category.</li>
<li>After each process in the pool finishes getting the videos for its assigned category, it will request up to 100 of the most recent comments and up to 100 of the most relevant comments for each video it received.</li>
<li>This results in up to 100 videos retrieved and up to 20,000 comments retrieved per available video category.</li>
<li>Each process will try to insert all the metadata it retrieved into the database.</li>
<li>Before the Program terminates, It prints the results of its execution.</li>
</ol>
</p>

<p>
<b>Things to know:</b><br>
<ol>
<li>Link to Youtube API V3 Documentation: https://developers.google.com/youtube/v3/docs</li>
<li>You can change the number of requested comments and videos by changing the constants (<span style="background-color:green;">NUMBER_OF_COMMENTS<span> and <span style="background-color:green;">NUMBER_OF_VIDEOS</span>)</li>
<li>If the assigned video category chart is not available, the process will be given a new category to request videos from.</li>
<li>The program will not insert comments that are already in the database.</li>
<li>The program will not insert videos that do not have any comments, have comments disabled, or </li>
<li>Our project can make up to 10,000 requests to the Youtube API every day.</li>
<li></li>
</ol>
</p>
