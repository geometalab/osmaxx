'use strict';
(function(){
    var ExcerptManager = function(locationFilter, inputElementsNewBoundingBox, selectElementExistingExcerpts, formElementPartsSwitcher) {
        this.locationFilter = locationFilter;
        this.inputElementsNewBoundingBox = inputElementsNewBoundingBox;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.formElementPartsSwitcher = formElementPartsSwitcher;


        /**
         * Synchronize coordinates in input fields to excerpt on map
         */
        this.updateInputElementsBoundingBox = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            this.inputElementsNewBoundingBox.inputElementNorth.value = locationFilterBounds._northEast.lat;
            this.inputElementsNewBoundingBox.inputElementWest.value = locationFilterBounds._southWest.lng;
            this.inputElementsNewBoundingBox.inputElementEast.value = locationFilterBounds._northEast.lng;
            this.inputElementsNewBoundingBox.inputElementSouth.value = locationFilterBounds._southWest.lat;
        };

        /**
         * Synchronize excerpt on map to coordinates in input fields
         */
        this.updateMapExcerpt = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            locationFilterBounds._northEast.lat = this.inputElementsNewBoundingBox.inputElementNorth.value;
            locationFilterBounds._southWest.lng = this.inputElementsNewBoundingBox.inputElementWest.value;
            locationFilterBounds._northEast.lng = this.inputElementsNewBoundingBox.inputElementEast.value;
            locationFilterBounds._southWest.lat = this.inputElementsNewBoundingBox.inputElementSouth.value;
            this.locationFilter.setBounds(locationFilterBounds);
        };
        
        this.isSelectOptionSelectedAndExcerptOnMapInSyncWithInputFields = function(select, locationFilterBounds) {
            if(select.value == "") {
                return false;
            }
            var optionElement = select.querySelector('option[value="'+select.value+'"]');
            return (
                optionElement.getAttribute('data-north') == locationFilterBounds._northEast.lat &&
                optionElement.getAttribute('data-west') == locationFilterBounds._southWest.lng &&
                optionElement.getAttribute('data-east') == locationFilterBounds._northEast.lng &&
                optionElement.getAttribute('data-south') == locationFilterBounds._southWest.lat
            );
        }

        /**
         * if the shown excerpt on the map changes and the change was not made by selecting an existing excerpt in the list
         * -> a user changed the excerpt, so change the form part to 'new-excerpt'
         */
        this.userChangeExcerptOnMapShowNewExcerptPart = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            var select = this.selectElementExistingExcerpts;
            if(!this.isSelectOptionSelectedAndExcerptOnMapInSyncWithInputFields(select, locationFilterBounds)) {
                this.formElementPartsSwitcher.value = 'new-excerpt';
                this.formElementPartsSwitcher.dispatchEvent(new Event('change'));
            }
        };


        // update coordinates input elements on change of excerpt on map
        this.locationFilter.on("change", function (event) {
            this.updateInputElementsBoundingBox();
            this.userChangeExcerptOnMapShowNewExcerptPart();
        }.bind(this));

        // update excerpt on map on change of coordinates input elements
        Object.keys(this.inputElementsNewBoundingBox).forEach(function(inputElementKey) {
            this.inputElementsNewBoundingBox[inputElementKey].addEventListener('change', this.updateMapExcerpt.bind(this));
        }.bind(this));

        // update excerpt on map on selection of existing excerpt in list
        this.selectElementExistingExcerpts.addEventListener('change', function(event) {
            var excerptOption = event.explicitOriginalTarget;
            if(excerptOption.getAttribute('data-geometry') == 'boundingbox') {
                var bounds = this.locationFilter.getBounds();
                bounds._northEast.lat = excerptOption.getAttribute('data-north');
                bounds._southWest.lng = excerptOption.getAttribute('data-west');
                bounds._northEast.lng = excerptOption.getAttribute('data-east');
                bounds._southWest.lat = excerptOption.getAttribute('data-south');
                this.locationFilter.setBounds(bounds);
                // enable excerpt on map for case it was disable before (e.g. by clicking on a not-boundingbox excerpt in the list)
                this.locationFilter.enable();
            } else {
                // no existing excerpt of type boundingbox -> disable excerpt because we are not able to show not-boundingbox excerpts on map
                this.locationFilter.disable();
            }
        }.bind(this));

        // enable excerpt on map on change of form mode (existing excerpt or new excerpt)
        this.formElementPartsSwitcher.addEventListener('change', function(event) {
            this.locationFilter.enable();
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
            inputElementNorth: document.getElementById('new_excerpt_bounding_box_north'),
            inputElementWest: document.getElementById('new_excerpt_bounding_box_west'),
            inputElementEast: document.getElementById('new_excerpt_bounding_box_east'),
            inputElementSouth: document.getElementById('new_excerpt_bounding_box_south')
        },
        document.getElementById('existing_excerpt.id'),
        document.getElementById('form-mode')
    );

    // push initial values to text inputs
    excerptManager.updateInputElementsBoundingBox();
})();
