var MongoClient = require('mongodb').MongoClient;
var http = require('http')

const url = "mongodb://10.251.12.108:30000?authSource=admin";

var str = "";
function connect_to_db(res) {
	MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
		var db = client.db("textual");

		var cursor = db.collection('RedditPosts').find();

		cursor.each(function(err, item) {
			if (item != null)
				res.write("Post Title: " + item.title + "<br/>");
			else
				res.end();
		});
	});
}

http.createServer(function (req, res) {
	res.writeHead(200, {'Content-Type': 'text/html'});
	res.write("REDDIT POSTS<br/>");
	connect_to_db(res);

}).listen(8080);

