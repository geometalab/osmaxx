window.objectToArray = function(nodeList) {
    return Object.keys(nodeList).map(function(index) {
        return nodeList[index];
    });
};

window.addEventMultipleListeners = function(node, eventNames, listener) {
    eventNames.forEach(function(eventName) {
        node.addEventListener(eventName, listener);
    });
};

jQuery.fn.filterGroups = function( options ) {
    // borrowed and adapted from https://gist.github.com/robcowie/2267793
    var $ = jQuery;
    var settings = $.extend({}, options);

    return this.each(function () {

        var $select = $(this);
        // Clone the optgroups to data, then remove them from dom
        $select.data('fg-original-groups', $select.find('optgroup').clone()).children('optgroup').remove();

        $(settings.groupSelector).change(function(){
            var $this = $(this);
            var optgroup_label = $this.val();
            var $optgroup =  $select.data('fg-original-groups');
            if (optgroup_label !== '') {
                $optgroup =  $optgroup.filter('optgroup[label="' + optgroup_label + '"]').clone();
            }
            $select.children('optgroup').remove();
            $select.append($optgroup);
        }).change();
    });
};
