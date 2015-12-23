window.ExcerptViewer = function(mapElementID, excerptApiUrl) {
    this.excerptApiUrl = excerptApiUrl;
    this.currentLayer = null;

    this.map = L.map(mapElementID).setView([0, 0], 2);
    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

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

    this.showExcerptOrCountryOnMap = function(ID) {
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
