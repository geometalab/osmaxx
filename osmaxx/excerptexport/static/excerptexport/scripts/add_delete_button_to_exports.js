'use strict';

(function(){
    jQuery(document).ready(function () {
        function _delete_export(export_id) {
            var panel_container = jQuery("#export-panel-" + export_id);
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

        var html_id = 'delete-export-';

        jQuery("div[id^=" + html_id + "]").each(function (discarded, elem) {
            var export_id = elem.id.replace(html_id, '');

            var delete_button = jQuery(elem);
            var group_title = delete_button.closest("div.panel-body").closest("div.panel").find(".panel-title").first();
            var existing_deletable_children = group_title.attr("deletable_children");
            if (existing_deletable_children === undefined) {
                group_title.attr("deletable_children", export_id);
            } else {
                group_title.attr("deletable_children", existing_deletable_children + "," + export_id);
            }
            if (group_title.attr('id') !== "delete-export-all") {
                group_title.attr("id", "delete-export-all");
                var excerpt_name = group_title.text();
                group_title.prepend('<span class="glyphicon glyphicon-trash hand-cursor" aria-hidden="true"></span> ');
                group_title.on('click', function () {
                    if (confirm('Are you sure you want to delete all deletable items of "' + excerpt_name + '"?')) {
                        var deletebale_ids = group_title.attr("deletable_children").split(',');
                        console.log(deletebale_ids);
                        deletebale_ids.forEach(function (export_id) {
                            _delete_export(export_id);
                        })
                    }
                });
            }

            delete_button.attr('class', '');
            delete_button.on('click', function (e, element) {
                var export_id = elem.id.replace(html_id, '');
                if (confirm('Are you sure you want to delete this?')) {
                    _delete_export(export_id);
                }
            });
        });
    });
})();
