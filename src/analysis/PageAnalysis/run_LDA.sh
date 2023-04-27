#!/bin/bash

for collection in RedditPosts_v2 RedditComments_v2 YelpReviews YoutubeVideo YoutubeComment WikiSourceText TwitterTweets ABC_Australia UrbanDictionary;
do
	echo $collection
	python3 LDAAnalysis.py $collection
done
