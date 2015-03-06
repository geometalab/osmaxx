/**
 * @author Raphael Das Gupta
 */
var map = L.map('map').setView([0, 0], 2);
// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var inputElementNorth = document.getElementById('excerpt.boundingBox.north');
var inputElementWest = document.getElementById('excerpt.boundingBox.west');
var inputElementEast = document.getElementById('excerpt.boundingBox.east');
var inputElementSouth = document.getElementById('excerpt.boundingBox.south');


var locationFilter = new L.LocationFilter({
    enable: true,
    enableButton: false
}).addTo(map);

function updateBboxTextInputsWith(bounds) {
    inputElementNorth.value = bounds._northEast.lat;
    inputElementWest.value = bounds._southWest.lng;
    inputElementEast.value = bounds._northEast.lng;
    inputElementSouth.value = bounds._southWest.lat;
}


// push initial values to text inputs
updateBboxTextInputsWith(locationFilter.getBounds());

// update text input values upon change on map
locationFilter.on("change", function (e) {
    console.log(locationFilter);
    console.log(locationFilter.getBounds())
    updateBboxTextInputsWith(e.bounds);
});


/**
 * update map on coordinate input field change
 */
function updateMapBoundingBox() {
    var bounds = locationFilter.getBounds();
    bounds._northEast.lat = inputElementNorth.value;
    bounds._southWest.lng = inputElementWest.value;
    bounds._northEast.lng = inputElementEast.value;
    bounds._southWest.lat = inputElementSouth.value;
    locationFilter.setBounds(bounds);
}

inputElementNorth.addEventListener('change', updateMapBoundingBox);
inputElementWest.addEventListener('change', updateMapBoundingBox);
inputElementEast.addEventListener('change', updateMapBoundingBox);
inputElementSouth.addEventListener('change', updateMapBoundingBox);