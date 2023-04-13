function initialize_downloads()
{
	fetch_collections();
	load_downloads();
}

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
                        var text = document_array[index]["text"];
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
/*
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
			var text = document_array[index]["text"];
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
*/
// Download the data displayed in JSON format
// This function should call on the search_downloads function on the backend of the website.
// Using a standard HTML input box, the user will be able to specify a collection to download from.
// Note: This function may have issues as I am unable to test the code without being inside the Linux lab currently.

function downloadData() {	
		
	//user_str, will be the string passed in from the frontend
	const user_opt = document.getElementById("user_download");
	const user_text = user_opt.options[user_opt.selectedIndex].text;
	const data = {collection: user_text};

	// Call the backend function to grab the specified content from the database.
	fetch("/search_downloads", {method: "POST", headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}, body: JSON.stringify(data)}).then(data => data.text()).then((documents) => {

	//Array to hold all the documents fetched from the database
	var document_array = JSON.parse(documents);
	var document_strings = JSON.stringify(document_array);

	//Create new blob of type JSON
	var blob = new Blob([document_strings], { type: "application/json" });	

	//Create a new link in the DOM and append the blob to it
	var a = document.createElement('a');
	a.download = user_text + ".json";
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

function fetch_collections()
{
	fetch("/collections", {method: "POST"}).then(data => data.text()).then((documents) => {
		//Array to hold all the collections fetched from the database.
		var collection_array = JSON.parse(documents);

		//Count how many documents are in the query
		const collection_length = collection_array.length;

		const user_opt = document.getElementById("user_download");
		
		for (var index = 0; index < collection_length; index++)
		{
			// Create selector element with the values pulled from the database
			var option = collection_array[index]["name"];
			var element = document.createElement("option");
			element.textContent = option;
			element.value = option;

			// Append the option the end of the select element
			user_opt.appendChild(element);
		}
	});
}

/*
// Download function for the neural network code
function downloadNetworkCode(file, text) {	 
	//creating an invisible element
	var element = document.createElement('a');
	element.setAttribute('href',
	'data:text/plain;charset=utf-8, '
	+ encodeURIComponent(text));
	element.setAttribute('download', file);
     
	// Above code is equivalent to
	// <a href="path of file" download="file name">
     
	document.body.appendChild(element);
     
	//onClick property
	element.click();
     
	document.body.removeChild(element);
    }
     
    // Start file download.
    document.getElementById("btn")
    .addEventListener("click", function() {
	// Generate download of hello.txt
	// file with some content
	var text = document.getElementById("text").value;
	var filename = "GFG.txt";
     
	download(filename, text);
    }, false);	
}
*/
