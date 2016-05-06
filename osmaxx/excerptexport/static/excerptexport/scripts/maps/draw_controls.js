var draw_controls = function (map) {
    // holds the geoJSON text representation
    var geoJSON_element = document.getElementById('id_bounding_geometry');
    geoJSON_element.parentNode.parentNode.className = "hidden";

    var editableLayers = new L.FeatureGroup();
    map.addLayer(editableLayers);

    var draw_enabled = {
        polyline: false,
        circle: false, // Turns off this drawing tool
        marker: false,
        polygon: {
            allowIntersection: false, // Restricts shapes to simple polygons
            drawError: {
                color: '#e1e100', // Color the shape will turn when intersects
                message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
            },
            shapeOptions: {
                color: 'black',
                fillOpacity: 0.15
            }
        },
        rectangle: {
            shapeOptions: {
                color: 'black',
                fillOpacity: 0.15
            }
        }
    };
    var options = {
        position: 'topright',
        draw: draw_enabled,
        edit: {
            featureGroup: editableLayers,
            remove: true
        }
    };
    var optionsDisabled = {
        position: 'topright',
        draw: false,
        edit: {
            featureGroup: editableLayers,
            remove: true
        }
    };

    var drawControlEnabled = new L.Control.Draw(options);
    var drawControlDisabled = new L.Control.Draw(optionsDisabled);

    drawControlEnabled.addTo(map);
    function updateGeoJSON (layer){
        geoJSON_element.value = JSON.stringify(layer.toGeoJSON()['geometry']);
    };

    map.on('draw:created', function (e) {
        drawControlDisabled.addTo(map);
        drawControlEnabled.removeFrom(map);
        var layer = e.layer;
        if (layer !== undefined) {
            editableLayers.addLayer(layer);
            map.fitBounds(layer.getBounds());
            updateGeoJSON(layer);
        }
    }.bind(this));

    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            if (layer !== undefined) {
                map.fitBounds(layer.getBounds());
                updateGeoJSON(layer);
            }
        });
    });

    map.on('draw:deleted', function () {
        geoJSON_element.value = '';
        if (editableLayers.getLayers().length === 0) {
            drawControlEnabled.addTo(map);
            drawControlDisabled.removeFrom(map);
        }
    });
};

