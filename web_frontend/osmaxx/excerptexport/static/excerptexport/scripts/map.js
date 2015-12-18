'use strict';
(function(){
    var ExcerptManager = function(locationFilter, inputElementsNewBoundingBox, selectElementExistingExcerpts, formElementPartsSwitcher) {
        this.locationFilter = locationFilter;
        this.inputElementsNewBoundingBox = inputElementsNewBoundingBox;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.formElementPartsSwitcher = formElementPartsSwitcher;
        this.selectedExcerptGeoJson = null;
        this.country = null;

        /**
         * Synchronize coordinates in input fields to excerpt on map
         */
        this.updateInputElementsBoundingBox = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            this.inputElementsNewBoundingBox.inputElementNorth.value = locationFilterBounds._northEast.lat;
            this.inputElementsNewBoundingBox.inputElementNorth.dispatchEvent(new Event('valueUpdate'));
            this.inputElementsNewBoundingBox.inputElementWest.value = locationFilterBounds._southWest.lng;
            this.inputElementsNewBoundingBox.inputElementWest.dispatchEvent(new Event('valueUpdate'));
            this.inputElementsNewBoundingBox.inputElementEast.value = locationFilterBounds._northEast.lng;
            this.inputElementsNewBoundingBox.inputElementEast.dispatchEvent(new Event('valueUpdate'));
            this.inputElementsNewBoundingBox.inputElementSouth.value = locationFilterBounds._southWest.lat;
            this.inputElementsNewBoundingBox.inputElementSouth.dispatchEvent(new Event('valueUpdate'));
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

        this.isSelectOptionSelectedAndExcerptOnMapInSyncWithInputFields = function(locationFilterBounds) {
            if (this.selectedExcerptGeoJson == null) {
                return false;
            }
            return (this.selectedExcerptGeoJson.getBounds().equals(locationFilterBounds));
        };

        /**
         * if the shown excerpt on the map changes and the change was not made by selecting an existing excerpt in the list
         * -> a user changed the excerpt, so change the form part to 'new-excerpt'
         */
        this.userChangeExcerptOnMapShowNewExcerptPart = function() {
            var locationFilterBounds = this.locationFilter.getBounds();
            if(!this.isSelectOptionSelectedAndExcerptOnMapInSyncWithInputFields(locationFilterBounds)) {
                this.formElementPartsSwitcher.value = 'new-excerpt';
                this.formElementPartsSwitcher.dispatchEvent(new Event('valueUpdate'));
                window.formPartManager.onFormPartsSwitcherChange();
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
        var getExcerptOptionAndUpdateFilter = function() {
            // we have single select, if it would happen to have two selected, ignore it.
            var excerptOption = document.querySelector( "#id_existing_excerpts option:checked");
            if(excerptOption) {
                this._setLocationFilterFromExcerptID(excerptOption.value);
            }
        }.bind(this);
        this.selectElementExistingExcerpts.addEventListener('click', getExcerptOptionAndUpdateFilter);
        this.selectElementExistingExcerpts.addEventListener('keyup', function(event) {
            // enter, arrow up or down
            if (event.keyCode == 13 || event.keyCode == 38 || event.keyCode == 40) {
                getExcerptOptionAndUpdateFilter();
            }
        });

        // enable excerpt on map on change of form mode (existing excerpt or new excerpt)
        this.formElementPartsSwitcher.addEventListener('change', function(event) {
            this.locationFilter.enable();
        }.bind(this));

        this._setLocationFilterFromExcerptID = function(ID) {
            var that = this;

            this._handleCountry = function (country){
                if (that.country !== null) {
                    map.removeLayer(that.country);
                }

                that.locationFilter.disable();
                that.country = that.selectedExcerptGeoJson;
                map.addLayer(that.country);
                map.fitBounds(country.getBounds());
            };

            this._handleBBoxBoundingGeometry = function (geometry){
                if (that.country !== null) {
                    map.removeLayer(that.country);
                }

                that.locationFilter.enable();
                that.locationFilter.setBounds(geometry.getBounds());
                map.fitBounds(that.locationFilter.getBounds());
            };

            this.selectedExcerptGeoJson = L.geoJson.ajax("/api/bounding_geometry_from_excerpt/"+ID+"/").on('data:loaded', function(){
                // We are certain that there is only one layer on this feature, because our API provides it so.
                var feature_type = this.getLayers()[0].feature.properties.type_of_geometry;
                switch(feature_type) {
                    case 'BBoxBoundingGeometry':
                        that._handleBBoxBoundingGeometry(this);
                        break;
                    case 'Country':
                        that._handleCountry(this);
                        break;
                    default:
                        break;
                }
            });
            this.selectedExcerptGeoJson.on('data:loading', function(){
                map.spin(true);
            });

            this.selectedExcerptGeoJson.on('data:loaded', function(){
                map.spin(false);
            });
        }.bind(this);
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
        },
        document.getElementById('id_existing_excerpts'),
        document.getElementById('id_form_mode')
    );

    // push initial values to text inputs
    excerptManager.updateInputElementsBoundingBox();
})();
