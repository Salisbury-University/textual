//var link = document.getElementByID("downloads_link");
//link.onClick = load_downloads;

function load_downloads()
{
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((documents) => {
		//var str = JSON.stringify(text, null, 2); // spacing level = 2
		//alert(documents);	
		//Write the the paragraph on the downloads page

		document.getElementById("downloads_content").innerHTML = documents;

	}).catch(function (error) {
		alert(error);
	});
}
