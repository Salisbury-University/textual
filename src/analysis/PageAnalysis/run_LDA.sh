#!/bin/bash

for collection in RedditPosts_v3 RedditComments_v3 YelpReviews YoutubeVideo YoutubeComment WikiSourceText AmazonReviews TwitterTweets;
do
	python3 LDAAnalysis.py $collection
done
