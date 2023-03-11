// Project Name(s): English Contextual Baseline Database
// Program Name: DataConnect.js
// Date: 11/10/2022-...
// Description: Connects to the MongoDB database from the HS Linux server and displays DB data on a localhost

//Import required packages
var MongoClient = require('mongodb').MongoClient;
var http = require('http');
var fs = require('fs');
var express = require('express');
var assert = require('assert');
var lineReader = require('line-reader');

//Database url, file is read in to avoid pushing login info to the GitHub
var url;

//Read the credentials from the mongodb file
lineReader.eachLine("mongo_credentials.txt", function(line, last) {
	url = line;
});

//Start the NodeJS express app, the contents of the page_content directory will be loaded
var app = express();
app.use(express.static(__dirname + "/page_content"));
//Start the app on port 8080
app.listen(8080);

//The function will be called when the user clicks on the downloads page
//Data will be posted, and can be fetched by the client to be displayed on the downloads page
app.post("/downloads", (req, res, next) => {
	try
	{
		//Connect to the database
		MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
			assert.equal(null, err);
			//Get the textual database
			const db = client.db("textual");

			//Create new promise
			var myPromise = () => {
				return new Promise((resolve, reject) => {
					//Query the database and convert the result to an array
					db.collection('RedditPosts').find().toArray(function(err, data) {
						err ? reject(err) : resolve(data);
					});
				});
			};

			//Setup async call
			var callMyPromise = async () => {
				var result = await (myPromise());
				return result;
			};

			callMyPromise().then(function(result) {
				//Close the connection to the database client
				client.close();
				
				//Send the query result to the client
				res.send(result);
			});
		}); //End of MongoClient call

	} catch (e) {
		next(e)
	}
});

app.post("/search_downloads", (req, res, next) => {
	try
	{
		//Connect to the database
		MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
			assert.equal(null, err);
			//Get the textual database
			const db = client.db("textual");

			//Create new promise
			var myPromise = () => {
				return new Promise((resolve, reject) => {
					//Query the database and convert the result to an array
					db.collection('RedditPosts').find().toArray(function(err, data) {
						err ? reject(err) : resolve(data);
					});
				});
			};

			//Setup async call
			var callMyPromise = async () => {
				var result = await (myPromise());
				return result;
			};

			callMyPromise().then(function(result) {
				//Close the connection to the database client
				client.close();
				
				//Send the query result to the client
				res.send(result);
			});
		}); //End of MongoClient call

	} catch (e) {
		next(e)
	}
});
