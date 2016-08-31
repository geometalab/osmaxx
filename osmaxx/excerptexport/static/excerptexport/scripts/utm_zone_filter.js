jQuery(document).ready(function(){
    var utm_optgroup_html_element = '#id_coordinate_reference_system optgroup[label="UTM zones"]',
        utm_zone_optgroup_original = jQuery(utm_optgroup_html_element).clone();

    window.filterUTMZones = function (leafletGeometry) {
        var utm_zone_optgroup = jQuery(utm_optgroup_html_element);

        if (utm_zone_optgroup !== null) {
            utm_zone_optgroup.html("");
            getUTMZones(leafletGeometry).done(function(data){
                var srids = data["utm_zone_srids"].sort(),
                    options_html = srids.map(function(srid){
                        return utm_zone_optgroup_original.find('option[value=' + srid + ']').prop('outerHTML');
                    }).join('');
                utm_zone_optgroup.html(options_html);
            }).fail(console.log);
        }

        function getUTMZones(leafletGeometry) {
            var geometry = leafletGeometry.toGeoJSON()["geometry"],
                srid = 4326,
                csrftoken = Cookies.get('csrftoken');
            return jQuery.ajax({
                url: '/api/utm-zone-info/',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                type: 'POST',
                data: JSON.stringify({"geom": geometry, "srid": srid}),
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });
        }
    };

});
