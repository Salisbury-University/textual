/*$(document).ready(function () {
    $("#database_table").DataTable();
});*/

function load_downloads()
{
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
		//Fetch the table from the HTML page
		var table = document.getElementById("database_table");
		table.style.tableLayout = "fixed";

		//Count how many documents are in the query
		const count = (documents.match(/\{(.*?)\}/g) || []).length;
		var index = 0;	

		//Array to hold all the documents fetched from the database (This way is 100x easier and super fast, I'm just stupid and didn't think of this before).
		var document_array = JSON.parse(documents);
		
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
			
			//Create a new row
			var row = table.insertRow();
			var cell_1 = row.insertCell(0);
			var cell_2 = row.insertCell(1);
			var cell_3 = row.insertCell(2);
			var cell_4 = row.insertCell(3);

			//Add data to the cells
			cell_1.innerHTML = title;
			cell_2.innerHTML = subreddit;
			cell_3.innerHTML = date;
			cell_4.innerHTML = text;

			index++;
		}
	}).catch(function (error) {
		alert(error);
	});
}
