var link = document.getElementByID("downloads_link");
link.onClick = load_downloads;

function load_downloads()
{
	fetch("/downloads", {method: "POST"});
}
