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
router=express.Router();
//Database url, file is read in to avoid pushing login info to the GitHub
var url;
//Read the credentials from the mongodb file
lineReader.eachLine("mongo_credentials.txt", function(line, last) {
	url = line;
});
//Start the NodeJS express app, the contents of the page_content directory will be loaded
var app = express();
const PORT = 3000;
app.use(express.static(__dirname + "/page_content"));
app.use(bodyParser.urlencoded({extended: true}));
//Start the app on port 8080
app.listen(8080);
//stores sources for search results
let sources=[];
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
app.get('/search', function(req, res) {
	res.render('search.html');
})

app.post('/search', function(req, res) {
	//res.writeHead(301, { Location: "http://localhost:8080/search_results.html" });
    	try
        {
                //Connect to the database
                MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
                        assert.equal(null, err);
                        //Get the textual database
                        const db = client.db("textual");
			/*db.listCollections().toArray(function(err, data) {
				let i =0;
				while (i<data.length){
					console.log(data[i]);
					i++;
				}
			});*/
                        //Create new promise
                        var myPromise = () => {
                                return new Promise((resolve, reject) => {
					collections=[];
					sources=[];
					if(typeof req.body.yelpCB!=='undefined'){
						collections.push('YelpReviews');
					}
					if(typeof req.body.redditCB!=='undefined'){
						collections.push('RedditPosts');
					}
					if(typeof req.body.youtubeCB!=='undefined'){
						collections.push('YoutubeComment');
					}
					if(typeof req.body.twitterCB!=='undefined'){
						collections.push('TwitterTweets');
					}
					if(typeof req.body.pgCB!=='undefined'){
						collections.push('PGText');
					}
					if(typeof req.body.wsCB!=='undefined'){
						collections.push('WikiSourceText');
					}
					if(typeof req.body.RC2CB!=='undefined'){
						collections.push('RedditComments_v2')
					}
					if(typeof req.body.amazonCB!=='undefined'){
						collections.push('AmazonReviews');
					}
					                                        //Query the database and convert the result to an array
                                        /*db.collection('YelpReviews').find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataYelp) {
						db.collection('RedditPosts').find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataReddit) {
							db.collection('YoutubeComment').find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err, dataYoutubeComments){
								err ? reject(err) : resolve(dataYelp.concat(dataReddit.concat(dataYoutubeComments)));
								//searchResults.concat(dataYelp.concat(dataReddit.concat(dataYoutubeComments)));
							});
						});
                                        });*/
					if(collections.length>0){
					db.collection(collections[0]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes1){
						if(collections.length>1){
						db.collection(collections[1]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes2){
							if(collections.length>2){
							db.collection(collections[2]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes3){
								if(collections.length>3){
								db.collection(collections[3]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes4){
									if(collections.length>4){
									db.collection(collections[4]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes5){
										if(collections.length>5){
										db.collection(collections[5]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes6){
											if(collections.length>6){
											db.collection(collections[6]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes7){
												if(collections.length>7){
												db.collection(collections[7]).find({text:{'$regex' : req.body.searchTerm, '$options' : 'i'}}).limit(3).toArray(function(err,sRes8){
													if(collections.length>8){
														console.log("uh oh");
													}
													else{
														for (let i = 0; i < sRes1.length; i++) {
                                        	                                                                        sources.push(collections[0]);
                                	                                                                        }
                        	                                                                                for (let i = 0; i < sRes2.length; i++) {
	                                                                                                                sources.push(collections[1]);
        	                                                                                                }
        		       	                                                                                for (let i = 0; i < sRes3.length; i++) {
                                                                                                        	        sources.push(collections[2]);
                                                                                                	        }
                                                                                        	                for (let i = 0; i < sRes4.length; i++) {
                                                                                	                                sources.push(collections[3]);
                                                                        	                                }
                                                                	                                        for (let i=0; i<sRes5.length; i++){
                                                        	                                                        sources.push(collections[4]);
                                                	                                                        }
                                        	                                                                for (let i=0; i<sRes6.length; i++){
                                	                                                                                sources.push(collections[5]);
                        	                                                                                }
                	                                                                                        for (let i=0; i<sRes7.length; i++){
        	                                                                                                        sources.push(collections[6]);
	                                                                                                        }
														for (let i=0; i<sRes8.length; i++){
															sources.push(collections[7]);
														}
														err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3.concat(sRes4.concat(sRes5.concat(sRes6.concat(sRes7.concat(sRes8))))))));
													}
												});
												}
												else{
													for (let i = 0; i < sRes1.length; i++) {
                                                                                                        	sources.push(collections[0]);
                                                                                                	}
                                                                                               		for (let i = 0; i < sRes2.length; i++) {
                                                                                                        	sources.push(collections[1]);
                                                                                                	}
                                                                                        	        for (let i = 0; i < sRes3.length; i++) {
                                                                                	                        sources.push(collections[2]);
                                                                        	                        }
                                                                	                                for (let i = 0; i < sRes4.length; i++) {
                                                        	                                                sources.push(collections[3]);
                                                	                                                }
                                        	                                                        for (let i=0; i<sRes5.length; i++){
                                	                                                                        sources.push(collections[4]);
                        	                                                                        }
                	                                                                                for (let i=0; i<sRes6.length; i++){
        	                                                                                                sources.push(collections[5]);
	                                                                                                }
													for (let i=0; i<sRes7.length; i++){
														sources.push(collections[6]);
													}
														err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3.concat(sRes4.concat(sRes5.concat(sRes6.concat(sRes7)))))));
												}
											});
											}
											else{
												for (let i = 0; i < sRes1.length; i++) {
                                                                                        	        sources.push(collections[0]);
                                                                                	        }
                                                                        	                for (let i = 0; i < sRes2.length; i++) {
                                                                	                                sources.push(collections[1]);
                                                        	                                }
                                                	                                        for (let i = 0; i < sRes3.length; i++) {
                                        	                                                        sources.push(collections[2]);
                                	                                                        }
                        	                                                                for (let i = 0; i < sRes4.length; i++) {
                	                                                                                sources.push(collections[3]);
        	                                                                                }
     	                                                                                   	for (let i=0; i<sRes5.length; i++){
                                                                                                	sources.push(collections[4]);
                                                                                        	}
												for (let i=0; i<sRes6.length; i++){
													sources.push(collections[5]);
												}
												err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3.concat(sRes4.concat(sRes5.concat(sRes6))))));
											}
										});					
									}
										else{
											for (let i = 0; i < sRes1.length; i++) {
                                                                                                sources.push(collections[0]);
                                                                                        }
                                                                                        for (let i = 0; i < sRes2.length; i++) {
                                                                                                sources.push(collections[1]);
                                                                                        }
                                                                                        for (let i = 0; i < sRes3.length; i++) {
                                                                                                sources.push(collections[2]);
                                                                                        }
                                                                                        for (let i = 0; i < sRes4.length; i++) {
                                                                                                sources.push(collections[3]);
                                                                                        }
											for (let i=0; i<sRes5.length; i++){
												sources.push(collections[4]);
											}
											err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3.concat(sRes4.concat(sRes5)))));
										}
									});
									}
									else{
											for (let i = 0; i < sRes1.length; i++) {
                                                                        			sources.push(collections[0]);
                                                                			}
                                                                			for (let i = 0; i < sRes2.length; i++) {
                                                                        			sources.push(collections[1]);
                                                        			        }
											for (let i = 0; i < sRes3.length; i++) {
                                                                        			sources.push(collections[2]);
                                                                			}
                                        		        	                for (let i = 0; i < sRes4.length; i++) {
                                	                	        	                sources.push(collections[3]);
        			                                                        }
	
											err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3.concat(sRes4))));
									}
								});
								}
								else{
									for (let i = 0; i < sRes1.length; i++) {
                                                                		sources.push(collections[0]);
                                                        		}
									for (let i = 0; i < sRes2.length; i++) {
                                                                		sources.push(collections[1]);
                                                        		}
									for (let i = 0; i < sRes3.length; i++) {
                                                                		sources.push(collections[2]);
                                                        		}
									err ? reject(err) : resolve(sRes1.concat(sRes2.concat(sRes3)));
								}
							});
							}
							else{
								for (let i = 0; i < sRes1.length; i++) {
                                                                	sources.push(collections[0]);
                                                        	}
								for (let i = 0; i < sRes2.length; i++) {
                                                                	sources.push(collections[1]);
                                                        	}
								err ? reject(err) : resolve(sRes1.concat(sRes2));
							}
						});
						}
						else{
	         				       /*fs.writeFile("search_results.json", JSON.stringify(sRes1),(err,resonse)=>{
         	                                       		if (err){
                                                       			console.error(err);
                                                        		return;
                                                		}
                                                		console.log("File has been created");
                                        	        	res.download("search_results.json");
							        console.log("TEST");
	                                        	});*/
							for (let i = 0; i < sRes1.length; i++) {
								sources.push(collections[0]);
							}
							err ? reject(err) : resolve(sRes1);
						}
					});
					}
					else{
						err ? reject(err) : resolve([]);
					}

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
				if(typeof req.body.downloadCB!=='undefined'){
                                        fs.writeFile("search_results.json", JSON.stringify(result),(err,resonse)=>{
                                                if (err){
                                                        console.error(err);
                                                        return;
                                                }
                                                console.log("File has been created");
						/*const filePath =`${__dirname}/files`;
                                		download("/mnt/linuxlab/home/jfernandez3/textual/src/website/search_results.json", filePath).then(()=>{
							console.log('File downloaded successfully!');
						})*/
						//res.pipe("search_results.json");
                                        });
                                }
				const firstHalf = fs.readFileSync(__dirname + "/search_results.html", "utf-8");
				firstHalf.split(/\r?\n/).forEach(line=> {
					res.write(line);
				});
				let ind=0;
				let author="Could not be found";
				let date="Could not be found";
				for (const textElement of result){
					author="Could not be found";
                                	date="Could not be found";
					if(typeof textElement.author!=='undefined'){
						console.log(textElement.author);
						author=textElement.author;
					}
					else if(typeof textElement.user_id!=='undefined'){
						author=textElement.user_id;
					}
					else if(typeof textElement.user!=='undefined'){
                                                author=textElement.user;
                                        }
					if(typeof textElement.date!=='undefined'){
						date=textElement.date;
					}
					else if(typeof textElement.Posted!=='undefined'){
                                                author=textElement.Posted;
                                        }
					else if(typeof textElement.publishDate!=='undefined'){
                                                author=textElement.publishDate;
                                        }
					res.write("<tr><td>"+sources[ind]+"</td><td>"+author+"</td><td>"+date+"</td><td>"+textElement.text.substring(0,1000)+"</td></tr>");
					ind=ind+1;
				}
				const secondHalf = fs.readFileSync(__dirname + "/search_results2.html","utf8");
				secondHalf.split(/\r?\n/).forEach(line=> {
                                        res.write(line);
                                });
				client.close();
                        	if(typeof req.body.downloadCB!=='undefined'){
					res.download("search_results.json");
				}
			});
				
                	}); //End of MongoClient call

        } catch (e) {
                next(e)
	}
})
