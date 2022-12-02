//var link = document.getElementByID("downloads_link");
//link.onClick = load_downloads;

function load_downloads()
{
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
		var content_string = "";
		
		/*
		var body = "";
		var header = "<title>Textual Baseline Database</title><style> body { background-color: #FFFFFF; } table { border: 1px solid black; } table td, table th { border: 2px solid black; } #pageHeader { margin: auto; text-align: center; border-bottom: 5px solid black; } #tableHeader { text-align: center; color: #FFFFFF; } </style>";
		content_string.concat("<!DOCTYPE html>" + "<html><head>" + header + "</head><body>" + body + "</body></html>");
		content_string.concat('<h1 id="pageHeader">COSC425/COSC426 Textual Baseline Database</h1><br/><br/>');
		content_string.concat('<h3 id="tableHeader">REDDIT POSTS</h3><br/>');

		content_string.concat("<table><tr>");
		content_string.concat("<th>Post Title</th><th>Subreddit</th><th>Post Date</th><th>Post Content</th></tr>");

		content_string.concat("<table><tr/>");
		*/
		//var str = JSON.stringify(text, null, 2); // spacing level = 2
		//alert(documents);	
		//Write the the paragraph on the downloads page		
		
		var index_start = documents.indexOf("{");
		var index_end = documents.indexOf("}") + 1;

		var sub_string = documents.substring(index_start, index_end);
		alert(sub_string);

		const json_obj = JSON.parse(sub_string);

		var title = json_obj.title;
		var text = json_obj.selftext;
		var subreddit = json_obj.subreddit;
		var date = json_obj.created_utc;

		document.getElementById("downloads_content").innerHTML = sub_string;
	
	}).catch(function (error) {
		alert(error);
	});
}
