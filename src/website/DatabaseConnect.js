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

function connect_to_db(res) {
	//Connect to the MongoDB
	MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
	

		//Print header and CSS
		var body = "";
		var header = "<title>Textual Baseline Database</title><style> body { background-color: #FFFFFF; } table { border: 1px solid black; } table td, table th { border: 2px solid black; } #pageHeader { margin: auto; text-align: center; border-bottom: 5px solid black; } #tableHeader { text-align: center; } </style>";
		res.write("<!DOCTYPE html>" + "<html><head>" + header + "</head><body>" + body + "</body></html>");
		res.write('<h1 id="pageHeader">COSC425/COSC426 Textual Baseline Database</h1><br/><br/>');
		res.write('<h3 id="tableHeader">REDDIT POSTS</h3><br/>');

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
				//res.end();
			}
		});
	});
}

var app = express();
app.use(express.static(__dirname + "/page_content"));
app.listen(8080);

app.get("/downloads", (req, res) => {
	connect_to_db(res);
});
/*
//Create local host server
http.createServer(function (req, res) {	
	//Print header
	
	var body = "";
	var header = "<title>Textual Baseline Database</title><style> body { background-color: #FFFFFF; } table { border: 1px solid black; } table td, table th { border: 2px solid black; } #pageHeader { margin: auto; text-align: center; border-bottom: 5px solid black; } #tableHeader { text-align: center; } </style>";
	res.write("<!DOCTYPE html>" + "<html><head>" + header + "</head><body>" + body + "</body></html>");
	res.write('<h1 id="pageHeader">COSC425/COSC426 Textual Baseline Database</h1><br/><br/>');
	res.write('<h3 id="tableHeader">REDDIT POSTS</h3><br/>');



	//Connect to database and print data
	//connect_to_db(res);

}).listen(8080); //Start the server
*/
