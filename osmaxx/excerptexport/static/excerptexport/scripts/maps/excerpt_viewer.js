window.ExcerptViewer = function(mapElementID, excerptApiUrl) {
    this.excerptApiUrl = excerptApiUrl;
    this.currentLayer = null;

    this.map = L.map(mapElementID).setView([0, 0], 2);

    L.control.scale().addTo(this.map);
    // add an OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

    this._handleCountryOrBBox = function (layer){
        if (this.currentLayer !== null) {
            this.map.removeLayer(this.currentLayer);
        }

        this.currentLayer = layer;
        this.map.addLayer(layer);

        window.addSizeEstimationToCheckboxes(layer);

    }.bind(this);

    this.showExcerptOnMap = function(ID) {
        L.geoJson.ajax(this.excerptApiUrl.replace('{ID}', ID)).on('data:loaded', function(event) {
            // We are certain that there is only one layer on this feature, because our API provides it so.
            var color = event.target.getLayers()[0].feature.properties.color || 'red';
            var layer = event.target;
            this._handleCountryOrBBox(layer);
            this.map.fitBounds(layer.getBounds());
            layer.setStyle({
                color: color,
                fillOpacity: 0.15
            });
        }.bind(this)).on('data:loading', function(){
            this.map.spin(true);
        }.bind(this)).on('data:loaded', function(){
            this.map.spin(false);
        }.bind(this));
    }.bind(this);

    this.disableZoom = function(){
        this.map.dragging.disable();
        this.map.touchZoom.disable();
        this.map.doubleClickZoom.disable();
        this.map.scrollWheelZoom.disable();
        this.map.keyboard.disable();
        if (this.map.tap) {
            this.map.tap.disable();
        }
    }.bind(this);
};
