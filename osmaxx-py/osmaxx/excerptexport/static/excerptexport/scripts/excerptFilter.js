"use strict";

(function() {
    jQuery.expr[':'].containsCI = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    jQuery(document).ready(function(){
        var excerptListFilterField = jQuery('input#excerptListFilterField');
        var excerptListFilterFieldClearer = jQuery('span#excerptListFilterFieldClearer');
        var excerptListFieldOptions = jQuery('select#existing_excerpt\\.id > optgroup > option');

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
            excerptListFilterFieldClearer.bind('click', function() {
                excerptListFilterField.val('');
                filterOptions(excerptListFilterField);
            });
            filterOptions(excerptListFilterField);
        }
    });
})();