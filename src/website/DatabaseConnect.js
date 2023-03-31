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
let bodyParser = require('body-parser');
//Database url, file is read in to avoid pushing login info to the GitHub
var url;

//Read the credentials from the mongodb file
lineReader.eachLine("mongo_credentials.txt", function(line, last) {
	url = line;
});
//Start the NodeJS express app, the contents of the page_content directory will be loaded
var app = express();
app.use(express.static(__dirname + "/page_content"));
app.use(bodyParser.urlencoded({extended: true}));
//Start the app on port 8080
app.listen(8080);
const searchResults=[];
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
app.get('/search2', function(req, res) {
	res.render('search2.html');
})

app.post('/search2', function(req, res) {
	console.log(req.body.searchTerm);
	//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });
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
					console.log(searchResults);
                                        //Query the database and convert the result to an array
                                        db.collection('YelpReviews').find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataYelp) {
						db.collection('RedditPosts').find({selftext:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataReddit) {
							db.collection('YoutubeComment').find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataYoutubeComments){
								err ? reject(err) : resolve(dataYelp.concat(dataReddit.concat(dataYoutubeComments)));
								//searchResults.concat(dataYelp.concat(dataReddit.concat(dataYoutubeComments)));
							});
						});
                                        });
					//err ? reject(err) : resolve(searchResults);
                                });
                        };

                        //Setup async call
                        var callMyPromise = async () => {
                                var result = await (myPromise());
                                return result;
                        };

                        callMyPromise().then(function(result) {
                                //Close the connection to the database client
				const firstHalf = fs.readFileSync(__dirname + "/search_results.html", "utf-8");
				firstHalf.split(/\r?\n/).forEach(line=> {
					res.write(line);
				});
				for (const textElement of result) {
					res.write("<tr><td>"+textElement.text+"</td></tr>");
				}
				const secondHalf = fs.readFileSync(__dirname + "/search_results2.html","utf8");
				secondHalf.split(/\r?\n/).forEach(line=> {
                                        res.write(line);
                                });
				client.close();
				res.send(result);
				//res.send(301, { Location: "http://localhost:8080/search2.html" });
				//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });

                        	});
                	}); //End of MongoClient call
			//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });

        } catch (e) {
                next(e)
	}
})
