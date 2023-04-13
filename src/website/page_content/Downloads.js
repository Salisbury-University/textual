// Project Name(s): English Contextual Baseline Database
// Program Name: DataConnect.js
// Date: 11/10/2022-...
// Description: Connects to the MongoDB database from the HS Linux server and displays DB data on a localhost

//Import required packages
var MongoClient = require('mongodb').MongoClient;
var http = require('http');
var fs = require('fs');
var express = require('express');

//Database url, does not contain the password for security purposes
const url = "mongodb://root:password@10.251.12.108:30000?authSource=admin";

window.onload = function(res) {
	//Connect to the MongoDB
	MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
		
		//Get the db from MongoDB and search the RedditPost collection
		var db = client.db("textual");
		var cursor = db.collection('RedditPosts').find();

		//Write table
		res.write("<table><tr>");
		res.write("<th>Post Title</th><th>Subreddit</th><th>Post Date</th><th>Post Content</th></tr>");
		
		//For each item, append it to the HTML content
		cursor.each(function(err, item) {
			//Write until empty
			if (item != null)
			{
				//Write post title, date, and text to the HTML page
				res.write("<tr><td>" + item.title + "</td>");
				res.write("<td>" + item.subreddit + "</td>");
				res.write("<td>" + item.created_utc + "</td>");
				var post_text = item.selftext;
				if (post_text == "")
					res.write("<td>" + "No Text Found" + "</td></tr>");
				else
					res.write("<td>" + post_text + "</td></tr>");
			}
			else
			{
				res.write("</table>");
				res.end();
			}
		});
	});
}
