"use strict";

(function() {
    /**
     * add case insensitive contains expression to jQuery
     */
    jQuery.expr[':'].containsCI = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    /**
     * filter listed excerpts by the filter word from the filter bar
     */
    jQuery(document).ready(function() {
        var excerptListFilterField = jQuery('input#excerptListFilterField');
        var excerptListFilterFieldClearer = jQuery('span#excerptListFilterFieldClearer');
        var excerptListFieldOptions = jQuery('select#id_existing_excerpts > optgroup > option');

        // hide all options and show the matching
        function filterOptions(excerptListFilterField) {
            var filterWord = excerptListFilterField.val();
            if (filterWord.length > 0) {
                excerptListFilterFieldClearer.show();
                excerptListFieldOptions.hide().filter(':containsCI('+filterWord+')').show();
            } else {
                excerptListFieldOptions.show();
                excerptListFilterFieldClearer.hide();
            }
        }

        if(excerptListFilterField && excerptListFilterFieldClearer) {
            excerptListFilterField.bind('change paste keyup input', function() {
                filterOptions(excerptListFilterField);
            });
            // clear field icon
            excerptListFilterFieldClearer.bind('click', function() {
                excerptListFilterField.val('');
                filterOptions(excerptListFilterField);
            });
            // execute filter for the first time -> may be there will be a filter word inside the filed after reload entered by the browser
            filterOptions(excerptListFilterField);
        }
    });
})();
