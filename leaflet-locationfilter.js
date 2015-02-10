/**
 * @author Raphael Das Gupta
 */

var locationFilter = new L.LocationFilter({
	enable : true
}).addTo(map);

function updateBboxTextInputsWith(bounds) {
	$('#input-north').val(bounds._northEast.lat);
	$('#input-west').val(bounds._southWest.lng);
	$('#input-east').val(bounds._northEast.lng);
	$('#input-south').val(bounds._southWest.lat);
}

// push initial values to text inputs
updateBboxTextInputsWith(locationFilter.getBounds());

// update text input values upon change on map
locationFilter.on("change", function(e) {
	updateBboxTextInputsWith(e.bounds);
});
