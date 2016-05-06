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
    }

    function showSizeOfLayer(layer) {
        estimateSize(layer).done(function (data) {
            function formatBytes(bytes) {
               if(bytes == 0) return '0 Byte';
               var k = 1000;
               var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
               var i = Math.floor(Math.log(bytes) / Math.log(k));
               return parseFloat((bytes / Math.pow(k, i)).toFixed()) + ' ' + sizes[i];
            }

            var estimatedFileSize = Number(data['estimated_file_size_in_bytes']);
            var e = document.getElementById('error_size_estimation_too_large');
            if (!e) {
                e = document.createElement('span');
                e.className = 'help-block';
                e.id = 'error_size_estimation_too_large';
                var bboxErrorField = document.getElementById('id_name');
                bboxErrorField.parentNode.appendChild(e);
            }
            if (isNaN(estimatedFileSize)) {
                e.innerHTML = '<strong>Invalid Area selected.</strong>';
            } else {
                e.innerHTML = '<strong>(Rough) Estimated File Size: ' + formatBytes(estimatedFileSize) + '</strong>';
            }

        });
    };

    map.on('draw:created', function (e) {
        drawControlDisabled.addTo(map);
        drawControlEnabled.removeFrom(map);
        var layer = e.layer;
        if (layer !== undefined) {
            showSizeOfLayer(layer);
            editableLayers.addLayer(layer);
            map.fitBounds(layer.getBounds());
            updateGeoJSON(layer);
        }
    }.bind(this));

    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            if (layer !== undefined) {
                showSizeOfLayer(layer);
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

