'use strict';

(function(){
    var ExcerptViewer = function(mapElementID, selectElementExistingExcerpts, excerptApiUrl) {
        this.excerptApiUrl = excerptApiUrl;
        this.selectElementExistingExcerpts = selectElementExistingExcerpts;
        this.currentLayer = null;

        this.map = L.map(mapElementID).setView([0, 0], 2);
        // add an OpenStreetMap tile layer
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        // update excerpt on map on selection of existing excerpt in list
        var getExcerptOptionAndUpdateFilter = function() {
            // we have single select, if it would happen to have two selected, ignore it.
            var excerptOption = this.selectElementExistingExcerpts.querySelector('option:checked');
            if(excerptOption) {
                this._showExcerptOrCountryOnMap(excerptOption.value);
            }
        }.bind(this);
        this.selectElementExistingExcerpts.addEventListener('click', getExcerptOptionAndUpdateFilter);
        this.selectElementExistingExcerpts.addEventListener('keyup', function(event) {
            // enter, arrow up or down
            if (event.keyCode == 13 || event.keyCode == 38 || event.keyCode == 40) {
                getExcerptOptionAndUpdateFilter();
            }
        });

        this._handleCountryOrBBox = function (layer){
            if (this.currentLayer !== null) {
                this.map.removeLayer(this.currentLayer);
            }

            this.currentLayer = layer;
            this.map.addLayer(layer);
        }.bind(this);

        this._extendBounds = function(bounds, marginFactor) {
            var latDiff = bounds._northEast.lat - bounds._southWest.lat;
            var lonDiff = bounds._northEast.lon - bounds._southWest.lon;
            bounds._northEast.lat += latDiff*marginFactor;
            bounds._southWest.lat -= latDiff*marginFactor;
            bounds._northEast.lon += lonDiff*marginFactor;
            bounds._southWest.lon -= lonDiff*marginFactor;
            return bounds;
        };

        this._showExcerptOrCountryOnMap = function(ID) {
            L.geoJson.ajax(this.excerptApiUrl.replace('{ID}', ID)).on('data:loaded', function(event) {
                // We are certain that there is only one layer on this feature, because our API provides it so.
                var feature_type = event.target.getLayers()[0].feature.properties.type_of_geometry;
                var layer = event.target;
                this._handleCountryOrBBox(layer);
                console.log(layer);
                switch(feature_type) {
                    case 'BBoxBoundingGeometry':
                        layer.setStyle({
                            color: 'black',
                            fillOpacity: 0.15
                        });
                        this.map.fitBounds(this._extendBounds(layer.getBounds(), 0.2));
                        break;
                    case 'Country':
                        layer.setStyle({
                            color: 'navy',
                            fillOpacity: 0.1
                        });
                        this.map.fitBounds(layer.getBounds());
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
