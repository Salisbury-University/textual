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
var bodyParser = require('body-parser'); // Used to get data from the frontend

//Database url, file is read in to avoid pushing login info to the GitHub
var url;

//Read the credentials from the mongodb file
lineReader.eachLine("mongo_credentials.txt", function(line, last) {
	url = line;
});
//Start the NodeJS express app, the contents of the page_content directory will be loaded
var app = express();

// Use the body-parser library
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(express.static(__dirname + "/page_content"));
app.use(bodyParser.urlencoded({extended: true}));
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
	// Get the user input value from the frontend
	const { collection } = req.body; // Get the user's requested collection from the frontend

	console.log('${collection}');
	
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
					//Use the user's requested collection
					db.collection('YelpReviews').find().limit(10000).toArray(function(err, data) {
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
/*
Gets the form data from the search page
let searchForm = document.getElementById("searchForm");
searchForm.addEventListener("submit", (e)=>{
	e.preventDefault();
	let searchTerm = document.getElementById("searchTerm");
	if (searchTerm.value == ""){
		alert("The term you searched for was empty. Please try again.");
	} else {
		console.log('You searched for ${searchTerm.value}');
	}
});
*/
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
                                        //Query the database and convert the result to an array
                                        db.collection('YelpReviews').find({ text: req.body.searchTerm}).limit(10000).toArray(function(err, data) {
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
				res.send(result);
				//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });

                        });
                }); //End of MongoClient call
		//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });

        } catch (e) {
                next(e)
	}
})
