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
		
		var index_start = documents.indexOf("{") + 1;
		var index_end = documents.indexOf("}");

		var sub_string = documents.substring(index_start, index_end);
		alert(sub_string);

		/*
		for (const character of documents)
		{
			if (character == "{")
				index_start = documents.indexOf(character);
			
			if (character == "}")
				end_index = documents.indexOf(character);			
		}

		alert("Output");
		*/

		//for (var i = 0; i < document_array.length; i++)
		//	document.getElementById("downloads_content").innerHTML = document_array[i] + "\n";
	
	}).catch(function (error) {
		alert(error);
	});
}
