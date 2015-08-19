/**
 * @author Raphael Das Gupta
 */
var map = L.map('map').setView([0, 0], 2);
// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var inputElementNorth = document.getElementById('new_excerpt_bounding_box_north');
var inputElementWest = document.getElementById('new_excerpt_bounding_box_west');
var inputElementEast = document.getElementById('new_excerpt_bounding_box_east');
var inputElementSouth = document.getElementById('new_excerpt_bounding_box_south');

var selectExistingExcerpts = document.getElementById('existing_excerpt.id');
var formPartsSwitcher = document.getElementById('form-mode');


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

/**
 * if the shown excerpt on the map changes and the change was not made by selecting an existing excerpt in the list -> a user changed the excerpt, so change the form part the
 */
function showNewExcerptPart(locationFilterBounds) {
    if(!(selectExistingExcerpts.value != "" &&
            selectExistingExcerpts.querySelector('option[value="'+selectExistingExcerpts.value+'"]').getAttribute('data-north') == locationFilterBounds._northEast.lat &&
            selectExistingExcerpts.querySelector('option[value="'+selectExistingExcerpts.value+'"]').getAttribute('data-west') == locationFilterBounds._southWest.lng &&
            selectExistingExcerpts.querySelector('option[value="'+selectExistingExcerpts.value+'"]').getAttribute('data-east') == locationFilterBounds._northEast.lng &&
            selectExistingExcerpts.querySelector('option[value="'+selectExistingExcerpts.value+'"]').getAttribute('data-south') == locationFilterBounds._southWest.lat)) {
        formPartsSwitcher.value = 'new-excerpt';
        formPartsSwitcher.dispatchEvent(new Event('change'));
    }
}


// push initial values to text inputs
updateBboxTextInputsWith(locationFilter.getBounds());

// update text input values upon change on map
locationFilter.on("change", function (e) {
    updateBboxTextInputsWith(e.bounds);
    showNewExcerptPart(e.bounds);
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

selectExistingExcerpts.addEventListener('change', function(event) {
    var excerptOption = event.explicitOriginalTarget;
    if(excerptOption.getAttribute('data-geometry') == 'boundingbox') {
        var bounds = locationFilter.getBounds();
        bounds._northEast.lat = excerptOption.getAttribute('data-north');
        bounds._southWest.lng = excerptOption.getAttribute('data-west');
        bounds._northEast.lng = excerptOption.getAttribute('data-east');
        bounds._southWest.lat = excerptOption.getAttribute('data-south');
        locationFilter.setBounds(bounds);
        locationFilter.enable();
    } else {
        locationFilter.disable();
    }
});

formPartsSwitcher.addEventListener('change', function(event) {
    locationFilter.enable();
});

