// Initiralize map
function initMap() {
	var options = {
		zoom: 8,
		center: {lat: 42.3601, lng: -71.0589}
	}

	var map = new google.map.Map(document.getElementById("map"), options)
}