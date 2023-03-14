"use strict";

(function() {
    jQuery('.resizable').each(function(count, el){
        var fixedWidth = jQuery(el).width();
        jQuery(el).resizable({
            minHeight: 100,
            minWidth: fixedWidth,
            maxWidth: fixedWidth
        });
    });

})();
