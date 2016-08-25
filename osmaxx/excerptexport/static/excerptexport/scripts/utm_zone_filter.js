window.filterUTMZones = function (leafletGeometry) {
    console.log(leafletGeometry);
    var utm_zone_optgroup = $('#id_coordinate_reference_system optgroup[label="UTM zones"]');

    if (utm_zone_optgroup !== null) {
        utm_zone_optgroup.html("");
        getUTMZones(leafletGeometry).done(function(data){
            var utm_zones = data["utm_zones"];

            utm_zones.sort(function(z1, z2){
                return z1.srid - z2.srid;
            });

            var options_html = '';
            utm_zones.forEach(function(zone){
                options_html += _optionHTML(zone.srid, zone.name);
            });
            utm_zone_optgroup.html(options_html);

        }).error(function(data, other, other2, other3){
            console.log(data, other, other2, other3);
        });
    }

    function getUTMZones(leafletGeometry) {
        var geometry = leafletGeometry.toGeoJSON()["geometry"];
        var csrftoken = Cookies.get('csrftoken');
        return jQuery.ajax({
            url: '/api/geodesy/utm-zones/',
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify({"geometry": geometry}),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    }

    function _optionHTML(srid, name) {
        return '<option value="' + srid + '">' + name + '</option>';

    }
};
