function load_downloads()
{
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
		//Fetch the table from the HTML page
		var table = document.getElementById("database_table");
		table.style.tableLayout = "fixed";

		//Count how many documents are in the query
		const count = (documents.match(/\{(.*?)\}/g) || []).length;
		var index = 0;

		//Loop through all the documents
		while(index < count)
		{
			//Get the starting and stopping indexes 
			var index_start = documents.indexOf("{");
			var index_end = documents.indexOf("}") + 1;

			//Get the substring and convert it to JSON
			var sub_string = documents.substring(index_start, index_end);
			const json_obj = JSON.parse(sub_string);

			//Get the values from the document
			var title = json_obj.title;
			var text = json_obj.selftext;
			var subreddit = json_obj.subreddit;
			var date = json_obj.created_utc;

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

			//Remove the value from the string
			documents = documents.replace(sub_string, "");
			index++;
		}
	}).catch(function (error) {
		alert(error);
	});
}
