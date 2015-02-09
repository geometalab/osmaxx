/**
 * @author Raphael Das Gupta
 */

var locationFilter = new L.LocationFilter({
	enable : true
}).addTo(map);

// push initial values to text inputs
var bounds = locationFilter.getBounds()
$('#input-north').val(bounds._northEast.lat);
$('#input-west').val(bounds._southWest.lng);
$('#input-east').val(bounds._northEast.lng);
$('#input-south').val(bounds._southWest.lat);

// update text input values upon change on map
locationFilter.on("change", function(e) {
	$('#input-north').val(e.bounds._northEast.lat);
	$('#input-west').val(e.bounds._southWest.lng);
	$('#input-east').val(e.bounds._northEast.lng);
	$('#input-south').val(e.bounds._southWest.lat);
});
