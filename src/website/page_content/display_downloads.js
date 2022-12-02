//var link = document.getElementByID("downloads_link");
//link.onClick = load_downloads;

function load_downloads()
{
	alert("TESING");
	fetch("/downloads", {method: "POST"}).then(data => data.text()).then((text) => {
		alert(text);
	}).catch(function (error) {
		alert(error);
	});
}
