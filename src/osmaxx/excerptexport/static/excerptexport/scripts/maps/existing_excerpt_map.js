'use strict';

(function(){
    window.addEventListener('load', function() {
        var existingExcerptSelectBox = document.getElementById('id_existing_excerpts');
        var excerptViewer = new ExcerptViewer(
            'map',
            "/api/bounding_geometry_from_excerpt/{ID}/"
        );

        var onExistingExcerptSelectBoxChange = function() {
            var excerptOption = existingExcerptSelectBox.querySelector('option:checked');
            if(excerptOption) {
                excerptViewer.showExcerptOnMap(excerptOption.value);
            }
        };

        existingExcerptSelectBox.addEventListener('click', onExistingExcerptSelectBoxChange);
        existingExcerptSelectBox.addEventListener('keyup', function(event) {
            // enter, arrow up or down
            if (event.keyCode == 13 || event.keyCode == 38 || event.keyCode == 40) {
                onExistingExcerptSelectBoxChange();
            }
        });
    });
})();
