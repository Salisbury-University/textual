function load_downloads()
{
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
		//Fetch the table from the HTML page
		var table = $("#database_table tbody");
		
		//Keep track of the current document
		var index = 0;	

		//Array to hold all the documents fetched from the database (This way is 100x easier and super fast, I'm just stupid and didn't think of this before).
		var document_array = JSON.parse(documents);
		
		//Count how many documents are in the query
		const count = document_array.length;

		//Loop through all the documents
		while(index < count)
		{
			//Get the values for each document. This includes the document title, text, category (subreddit), and the date.
			var title = document_array[index]["title"];
			var text = document_array[index]["selftext"];
			var subreddit = document_array[index]["subreddit"];
			var date = document_array[index]["created_utc"];

			//If the text from the query is empty, write a message
			if (text == "")
				text = "No Text Found.";	

			//Create a new row with the current content
			var row = $("<tr><td>" + title + "</td><td>" + subreddit + "</td><td>" + date + "</td><td>" + text + "</td></tr>");

			//Append the new row to the table
			table.append(row);

			//Increment the number of pages
			index++;
		}

		//Create the bootstrap table dynamically
		$("#database_table").DataTable();
		$('.dataTables_length').addClass('bs-select');
	}).catch(function (error) {
		alert(error);
	});
}

//Download the data displayed in JSON format
function downloadData() {	
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
	
	//Array to hold all the documents fetched from the database
	var document_array = JSON.parse(documents);
	var document_strings = JSON.stringify(document_array);

	//Create new blob of type JSON
	var blob = new Blob([document_strings], { type: "application/json" });	

	//Create a new link in the DOM and append the blob to it
	var a = document.createElement('a');
	a.download = "RedditPosts.json";
	a.href = URL.createObjectURL(blob);
	a.dataset.downloadurl = ["application/json", a.download, a.href].join(':');
	a.style.display = "none";
	document.body.appendChild(a);

	//Click the link to download the file
	a.click();
	//Remove the DOM element
	document.body.removeChild(a);
	
	//Set new timeout
	setTimeout(function() { URL.revokeObjectURL(a.href); }, 1500);
	}).catch(function (error) {
		alert(error);
	});
}
