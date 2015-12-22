'use strict';

(function(){
    var ExcerptViewer = function(mapElementID, selectElementExistingExcerpts, excerptApiUrl) {
        this.excerptApiUrl = excerptApiUrl;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.currentCountryLayer = null;

        this.map = L.map(mapElementID).setView([0, 0], 2);
        // add an OpenStreetMap tile layer
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        this.locationFilter = new L.LocationFilter({
            enable: false,
            enableButton: false
        }).addTo(this.map);


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

        this._handleCountry = function (country){
            if (this.currentCountryLayer !== null) {
                this.map.removeLayer(this.currentCountryLayer);
            }

            this.locationFilter.disable();
            this.currentCountryLayer = country;
            this.map.addLayer(country);
            this.map.fitBounds(country.getBounds());
        }.bind(this);

        this._handleBBoxBoundingGeometry = function (geometry){
            if (this.currentCountryLayer !== null) {
                this.map.removeLayer(this.currentCountryLayer);
            }

            // If location filter is enabled, it will collide with fitBounds and you will get some strange behaviour
            this.locationFilter.disable();
            this.locationFilter.setBounds(geometry.getBounds());
            this.map.fitBounds(geometry.getBounds());
            this.locationFilter.enable();
        }.bind(this);

        this._setLocationFilterFromExcerptID = function(ID) {
            L.geoJson.ajax(this.excerptApiUrl.replace('{ID}', ID)).on('data:loaded', function(event) {
                // We are certain that there is only one layer on this feature, because our API provides it so.
                var feature_type = event.target.getLayers()[0].feature.properties.type_of_geometry;
                switch(feature_type) {
                    case 'BBoxBoundingGeometry':
                        this._handleBBoxBoundingGeometry(event.target);
                        break;
                    case 'Country':
                        this._handleCountry(event.target);
                        break;
                    default:
                        break;
                }
            }.bind(this)).on('data:loading', function(){
                this.map.spin(true);
            }.bind(this)).on('data:loaded', function(){
                this.map.spin(false);
            }.bind(this));
        }.bind(this);
    };


    window.addEventListener('load', function() {
        new ExcerptViewer(
            'map',
            document.getElementById('id_existing_excerpts'),
            "/api/bounding_geometry_from_excerpt/{ID}/"
        );
    });
})();
