window.filterUTMZones = function (leafletGeometry) {
    var getUTMZones = function (leafletGeometry) {
        console.log(leafletGeometry.getLayers()[0].feature.geometry);
        // console.log(leafletGeometry.getLayers()[0].geometry.toGeoJSON());
        var csrftoken = Cookies.get('csrftoken');
            return jQuery.ajax({
                url: '/api/geodesy/utm-zones/',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                type: 'POST',
                data: JSON.stringify({"geometry": leafletGeometry.getLayers()[0].feature.geometry}),
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
                // success: function() {
                //     panel_container.remove();
                // }
            });
    };

    getUTMZones(leafletGeometry).done(function(data, other, other2, other3){
        console.log(data, other, other2, other3);
    }).error(function(data, other, other2, other3){
            console.log(data, other, other2, other3);
        });
};
