// Project Name(s): English Contextual Baseline Database
// Program Name: DataConnect.js
// Date: 11/10/2022-...
// Description: Connects to the MongoDB database from the HS Linux server and displays DB data on a localhost

//Import required packages
var MongoClient = require('mongodb').MongoClient;
var http = require('http')

//Database url, does not contain the password for security purposes
const url = "mongodb://10.251.12.108:30000?authSource=admin";

function connect_to_db(res) {
	//Connect to the MongoDB
	MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
		
		//Get the db from MongoDB and search the RedditPost collection
		var db = client.db("textual");
		var cursor = db.collection('RedditPosts').find();

		//For each item, append it to the HTML content
		cursor.each(function(err, item) {
			//Write until empty
			if (item != null)
				res.write("Post Title: " + item.title + "<br/>");
			else
				res.end();
		});
	});
}

//Create local host server
http.createServer(function (req, res) {
	//Print header
	res.writeHead(200, {'Content-Type': 'text/html'});
	res.write("REDDIT POSTS<br/>");
	//Connect to database and print data
	connect_to_db(res);

}).listen(8080); //Start the server
