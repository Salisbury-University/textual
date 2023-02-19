// Project Name(s): English Contextual Baseline Database
// Program Name: DataConnect.js
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
		var cursor = db.collection('YelpReviews').find();

		//Write table
		res.write("<table><tr>");
		res.write("<th>Stars</th><th>Text</th><th>Date</th><th>Database</th></tr>");

		//For each item, append it to the HTML content
		cursor.each(function(err, item) {
			//Write until empty
			if (item != null)
			{
				//Write post title, date, and text to the HTML page
				res.write("<tr><td>" + item.stars + "</td>");
				var source_text = item.text;
				if (source_text == "")
					res.write("<td>" + "No Text Found" + "</td>");
				else
					res.write("<td>" + source_Text + "</td>");
				res.write("<td>"+item.stars+"</td>")
				res.write("<td>YelpReviews</td></tr>")
			}
			else
			{
				res.write("</table>");
				res.end();
			}
		});
	});
}
