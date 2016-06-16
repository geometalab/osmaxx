'use strict';

(function(){
    jQuery(document).ready(function () {
        var html_id = 'delete-export-';
        jQuery("div[id^=" + html_id + "]").each(function (discarded, elem) {
            var delete_button = jQuery(elem);
            delete_button.attr('class', '');
            delete_button.on('click', function (e, element) {
                var export_id = elem.id.replace(html_id, ''),
                    panel_container = jQuery("#export-panel-" + export_id);

                if (confirm('Are you sure you want to delete this?')) {
                    var csrftoken = Cookies.get('csrftoken');
                    jQuery.ajax({
                        url: '/api/exports/' + export_id + '/',
                        dataType: 'json',
                        type: 'DELETE',
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        success: function() {
                            panel_container.remove();
                        }
                    });
                }
            });
        });
    });
})();
