'use strict';
(function(){
    var map = L.map('map', {worldCopyJump: true}).setView([0, 0], 2);
    // add an OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    L.control.scale().addTo(map);
    draw_controls(map);
})();
