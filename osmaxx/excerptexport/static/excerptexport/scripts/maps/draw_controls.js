var draw_controls = function (map) {
    L.drawLocal.draw.toolbar.buttons.polygon = 'Select freehand area';
    L.drawLocal.draw.toolbar.buttons.rectangle = 'Select rectangular area';
    L.drawLocal.edit.toolbar.buttons.edit = 'Edit selection';
    L.drawLocal.edit.toolbar.buttons.editDisabled = 'No selection to edit';
    L.drawLocal.edit.toolbar.buttons.remove = 'Delete selection';
    L.drawLocal.edit.toolbar.buttons.removeDisabled = 'No selection to delete';
    L.drawLocal.edit.handlers.remove.tooltip.text = 'Click on the extent area to remove it';
    // holds the geoJSON text representation
    var geoJSON_element = document.getElementById('id_bounding_geometry');
    geoJSON_element.parentNode.parentNode.className = "hidden";

    var detailLevelID = '#id_detail_level';

    var editableLayers = new L.FeatureGroup();
    map.addLayer(editableLayers);

    var SelectCurrentExtentControl = L.Control.extend({
        options: {
            position: 'topright'
            //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
        },
        initialize: function (text, options) {
            L.Util.setOptions(this, options);
            this.container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-current-extent');
            this.container.innerHTML = text;
        },
        onAdd: function (map) {
            this.container.style.backgroundColor = 'white';
            this.container.onclick = function(){
                var rectangle = L.rectangle(map.getBounds());
                map.zoomOut();
                map.fire('draw:created', { layer: rectangle, layerType: 'rectangle' });
            };
            return this.container;
        }
    });

    var draw_enabled = {
        polyline: false,
        circle: false, // Turns off this drawing tool
        marker: false,
        polygon: {
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
    var ourCustomControl = new SelectCurrentExtentControl('Select current extent');
    drawControlEnabled.addTo(map);
    ourCustomControl.addTo(map);
    function updateGeoJSON (layer){
        geoJSON_element.value = JSON.stringify(layer.toGeoJSON()['geometry']);
    }

    function showSizeOfLayer(layer) {
        var allowedMaxSize = 1024 * 1024 * 1024;  // 1 GB in bytes, approx. 1/5 of Germany, estimation of the PBF size
        var allowedMaxSizeSimplified = 3 * allowedMaxSize;  // 3 GB in bytes, approx. 1/2 of Germany, estimation of the PBF size
        var simplifiedSelectValue = "60";
        var nameField = document.getElementById('id_name');

        var e = document.getElementById('error_size_estimation_too_large');
        if (!e) {
            e = document.createElement('span');
            e.className = 'help-block';
            e.id = 'error_size_estimation_too_large';
            nameField.parentNode.appendChild(e);
        }

        function _getSelectedDetailLevel() {
            return jQuery(detailLevelID).find(":selected").attr('value');
        }

        function getAllowedMaxSize(){
            var selectedValue = _getSelectedDetailLevel();
            if (parseInt(selectedValue) === 60) {
                return allowedMaxSizeSimplified;
            }
            return allowedMaxSize;
        }

        function isSimplifiedChosen() {
            var selectedDetailLevel = _getSelectedDetailLevel();
            return selectedDetailLevel === simplifiedSelectValue;
        }

        function encourageUserToSwitchToLowerDetails() {
            if (!isSimplifiedChosen()) {
                var originalBGColor = jQuery(detailLevelID).css("background-color");
                var originalTextColor = jQuery(detailLevelID).css("color");
                jQuery(detailLevelID).animate({
                  backgroundColor: "#F8D568",
                  color: "#B7410E"
                }, 500 );
                jQuery(detailLevelID).animate({
                  backgroundColor: originalBGColor,
                  color: originalTextColor
                }, 500 );
            }
        }

        function isExtentTooLarge(estimatedFileSize) {
            return estimatedFileSize > getAllowedMaxSize();
        }

        addSizeEstimationToCheckboxes(layer);
        estimateSize(layer).done(function (data) {
            var estimatedFileSize = Number(data['estimated_file_size_in_bytes']);

            var message_html = '';
            if (isExtentTooLarge(estimatedFileSize)) {
                encourageUserToSwitchToLowerDetails();
                var howMuchTooLarge = estimatedFileSize ? Math.ceil(estimatedFileSize * 100 / getAllowedMaxSize() - 100) + '% ' : '';
                var message = 'Excerpt {percent}too large!'.replace('{percent}', howMuchTooLarge);

                if (!isSimplifiedChosen()) {
                    message += ' Switching to the simplified data-model allows larger extends.';
                }
                message_html = '<strong>' + message + '<br />';
                nameField.setCustomValidity(message);
            } else {
                nameField.setCustomValidity('');
            }

            if (isNaN(estimatedFileSize)) {
                e.innerHTML = '<strong>Invalid Area selected.</strong>';
            } else {
                e.innerHTML = message_html;
            }

        });
    }

    map.on('draw:created', function (e) {
        drawControlDisabled.addTo(map);
        drawControlEnabled.removeFrom(map);
        ourCustomControl.removeFrom(map);
        var layer = e.layer;
        if (layer !== undefined) {
            jQuery( detailLevelID ).change(function() {
                    showSizeOfLayer(layer);
            });
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
        jQuery( detailLevelID ).off( "change" );
        geoJSON_element.value = '';
        if (editableLayers.getLayers().length === 0) {
            drawControlEnabled.addTo(map);
            drawControlDisabled.removeFrom(map);
            ourCustomControl.addTo(map);
        }
    });
};
