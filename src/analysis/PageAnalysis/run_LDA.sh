#!/bin/bash

for collection in RedditPosts_v2 RedditComments_v2 YelpReviews YoutubeVideo YoutubeComment WikiSourceText AmazonReviews TwitterTweets ABC_Australia UrbanDictionary MoreAmazon;
do
	python3 LDAAnalysis.py $collection
done
