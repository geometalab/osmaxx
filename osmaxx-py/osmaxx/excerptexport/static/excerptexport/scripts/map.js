'use strict';
(function(){
    var ExcerptManager = function(locationFilter, inputElementsNewBoundingBox, selectElementExistingExcerpts, formElementPartsSwitcher) {
        this.locationFilter = locationFilter;
        this.inputElementsNewBoundingBox = inputElementsNewBoundingBox;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.formElementPartsSwitcher = formElementPartsSwitcher;
        this.selectedExcerptGeoJson = null;

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
            if (select.value == "" || this.selectedExcerptGeoJson == null) {
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
        this.selectElementExistingExcerpts.addEventListener('change', function() {
            // we have single select, if it would happen to have two selected, ignore it.
            var excerptOption = $( "select[id=id_existing_excerpts] option:selected")[0];
            this._setLocationFilterFromExcerptID(excerptOption.value);
        }.bind(this));

        // enable excerpt on map on change of form mode (existing excerpt or new excerpt)
        this.formElementPartsSwitcher.addEventListener('change', function(event) {
            this.locationFilter.enable();
        }.bind(this));

        this._setLocationFilterFromExcerptID = function(ID) {
            var that = this;
            this.selectedExcerptGeoJson = L.geoJson.ajax("/api/bounding_geometry_from_excerpt/"+ID+"/").on('data:loaded', function(){
                //TODO: differentiate between boundingbox or country and similar
                // if is boundingbox
                //    this.locationFilter.enable();
                // if is polygon
                //    this.locationFilter.disable();
                that.locationFilter.setBounds(this.getBounds());
                map.fitBounds(that.locationFilter.getBounds());
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
