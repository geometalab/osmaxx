(function () {
    window.estimateSize = function (leafletGeometry) {
        var latLngs = leafletGeometry.getBounds(),
            north = latLngs.getNorth(),
            east = latLngs.getEast(),
            south = latLngs.getSouth(),
            west = latLngs.getWest();
        return jQuery.getJSON(
            '/api/estimated_file_size/',
            {
                'north': north,
                'east': east,
                'south': south,
                'west': west
            });
    };

    window.formatBytes = function (bytes) {
        if (bytes === 0) {
            return '0 Byte';
        }
        var k = 1000;
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        var i = Math.min(Math.floor(Math.log(bytes) / Math.log(k)), sizes.length - 1);
        return parseFloat((bytes / Math.pow(k, i)).toFixed()) + ' ' + sizes[i];
    };

    function _addToCheckboxes(data) {
        var checkboxes = jQuery("#div_id_formats input[type='checkbox']");
        checkboxes.each(function (_, checkbox) {
            var format = jQuery(checkbox).attr('value');
            var size = formatBytes(data[format]);
            var sizeText = "<span class='size_estimation'> (~" + size + ")</span>";
            var label = checkbox.parentElement;
            var placement = jQuery(label).find("span[class='size_estimation']");
            if (placement.length > 0) {
                jQuery(placement).html(sizeText);
            } else {
                jQuery(label).append(sizeText);
            }
        });
    }

    window.addSizeEstimationToCheckboxes = function (layer) {
        var estimateSizeForFormats = function (pbfSize, detailLevel) {
            return jQuery.getJSON(
                '/api/format_size_estimation/',
                {
                    'estimated_pbf_file_size_in_bytes': pbfSize,
                    'detail_level': detailLevel
                });
        };
        estimateSize(layer).done(function (data) {
            var pbfSize = data['estimated_file_size_in_bytes'];
            var detailLevel = jQuery("#id_detail_level").find(":selected").attr('value');
            if (detailLevel != null) {
                estimateSizeForFormats(pbfSize, detailLevel).done(function (data) {
                    _addToCheckboxes(data);
                });
            }
        });
    };
})();
