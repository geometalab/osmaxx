'use strict';
(function(){
    var ExcerptManager = function(locationFilter, inputElementsNewBoundingBox) {
        this.locationFilter = locationFilter;
        this.inputElementsNewBoundingBox = inputElementsNewBoundingBox;

        /**
         * Synchronize coordinates in input fields to excerpt on map
         */
        this.updateInputElementsBoundingBox = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            this.inputElementsNewBoundingBox.inputElementNorth.value = locationFilterBounds._northEast.lat;
            this.inputElementsNewBoundingBox.inputElementNorth.dispatchEvent(new CustomEvent("valueUpdate"));
            this.inputElementsNewBoundingBox.inputElementWest.value = locationFilterBounds._southWest.lng;
            this.inputElementsNewBoundingBox.inputElementWest.dispatchEvent(new CustomEvent("valueUpdate"));
            this.inputElementsNewBoundingBox.inputElementEast.value = locationFilterBounds._northEast.lng;
            this.inputElementsNewBoundingBox.inputElementEast.dispatchEvent(new CustomEvent("valueUpdate"));
            this.inputElementsNewBoundingBox.inputElementSouth.value = locationFilterBounds._southWest.lat;
            this.inputElementsNewBoundingBox.inputElementSouth.dispatchEvent(new CustomEvent("valueUpdate"));
        };
        this.areAllBoxesSet = function(){
            return this.inputElementsNewBoundingBox.inputElementNorth.value &&
                this.inputElementsNewBoundingBox.inputElementWest.value &&
                this.inputElementsNewBoundingBox.inputElementEast.value &&
                this.inputElementsNewBoundingBox.inputElementSouth.value
        }.bind(this);

        /**
         * Synchronize excerpt on map to coordinates in input fields
         */
        this.updateMapExcerpt = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            locationFilterBounds._northEast.lat = this.inputElementsNewBoundingBox.inputElementNorth.value;
            locationFilterBounds._southWest.lng = this.inputElementsNewBoundingBox.inputElementWest.value;
            locationFilterBounds._northEast.lng = this.inputElementsNewBoundingBox.inputElementEast.value;
            locationFilterBounds._southWest.lat = this.inputElementsNewBoundingBox.inputElementSouth.value;
            if (this.areAllBoxesSet()) {
                this.locationFilter.setBounds(locationFilterBounds);
            }
        };

          // update coordinates input elements on change of excerpt on map
        this.locationFilter.on("change", function (event) {
            this.updateInputElementsBoundingBox();
        }.bind(this));

        // update excerpt on map on change of coordinates input elements
        Object.keys(this.inputElementsNewBoundingBox).forEach(function(inputElementKey) {
            this.inputElementsNewBoundingBox[inputElementKey].addEventListener('change', this.updateMapExcerpt.bind(this));
        }.bind(this));
    };

    var map = L.map('map').setView([0, 0], 2);
    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var locationFilter = new L.LocationFilter({
        enable: true,
        enableButton: false
    }).addTo(map);

    var excerptManager = new ExcerptManager(
        locationFilter,
        {
            inputElementNorth: document.getElementById('id_north'),
            inputElementWest: document.getElementById('id_west'),
            inputElementEast: document.getElementById('id_east'),
            inputElementSouth: document.getElementById('id_south')
        }
    );

    // push initial values to text inputs
    excerptManager.updateInputElementsBoundingBox();
})();
