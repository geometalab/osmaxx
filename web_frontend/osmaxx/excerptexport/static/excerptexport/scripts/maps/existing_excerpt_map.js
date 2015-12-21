'use strict';

(function(){
    var ExcerptViewer = function(locationFilter, selectElementExistingExcerpts) {
        this.locationFilter = locationFilter;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.selectedExcerptGeoJson = null;
        this.country = null;


        // update excerpt on map on selection of existing excerpt in list
        var getExcerptOptionAndUpdateFilter = function() {
            // we have single select, if it would happen to have two selected, ignore it.
            var excerptOption = this.selectElementExistingExcerpts.querySelector('option:checked');
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

        // TODO: Replace this not understandable hack
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

                // If location filter is enabled, it will collide with fitBounds and you will get some strange behaviour
                that.locationFilter.disable();
                that.locationFilter.setBounds(geometry.getBounds());
                map.fitBounds(geometry.getBounds());
                that.locationFilter.enable();
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
        enable: false,
        enableButton: false
    }).addTo(map);

    var excerptManager = new ExcerptViewer(
        locationFilter,
        document.getElementById('id_existing_excerpts')
    );
})();
