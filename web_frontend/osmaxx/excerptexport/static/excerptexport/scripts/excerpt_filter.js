"use strict";

(function() {
    // borrowed from http://codepen.io/gapcode/pen/vEJNZN, condensed
    function detectIE() {
        var ua = window.navigator.userAgent;
        return (ua.indexOf('MSIE ') > 0) || (ua.indexOf('Trident/') > 0) || (ua.indexOf('Edge/') > 0);
    }

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

        var hideElements = function(filterWord) {
            excerptListFilterFieldClearer.show();
            excerptListFieldOptions.hide().filter(':containsCI(' + filterWord + ')').show();
        };
        var showAllElements = function() {
            excerptListFieldOptions.show();
            excerptListFilterFieldClearer.hide();
        };

        // ################# IE patch... #################
        // Inspired by: http://ajax911.com/hide-options-selecbox-jquery/
        if (detectIE()) {
            showAllElements = function() {
                excerptListFieldOptions.each(function(index, val) {
                    if (this.nodeName.toUpperCase() === 'OPTION') {
                        var span = $(this).parent();
                        var opt = this;
                        if ($(this).parent().is('span')) {
                            $(opt).show();
                            $(span).replaceWith(opt);
                        }
                    }
                });
            };

            //hide elements
            hideElements = function(filterWord) {
                excerptListFieldOptions.each(function(index, val) {
                    // wrap all
                    if ($(this).is('option') && (!$(this).parent().is('span'))) {
                        $(this).wrap('<span>');
                    }
                });
                var selectIEOptions = jQuery('select#id_existing_excerpts > optgroup > span > option');
                // unwrap matching ones
                selectIEOptions.filter(':containsCI(' + filterWord + ')').each(function(){
                    var elem = $(this);
                        var span = elem.parent();
                        $(elem).show();
                        $(span).replaceWith(elem);
                });
            };
        }
        // ################# ...IE patch end #################

        function filterOptions(excerptListFilterField) {
            var filterWord = excerptListFilterField.val();
            if (filterWord.length > 0) {
                hideElements(filterWord);
            } else {
                showAllElements();
            }
        }

        if (excerptListFilterField && excerptListFilterFieldClearer) {
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
