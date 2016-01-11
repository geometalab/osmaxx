(function(){
    /**
     * Uses html5 setCustomValidity()
     * The browser will disable the submit button by it's own if some element contains an error message set by setCustomValidity()
     */
    var FormValidator = function(bboxFields, excerptBoundsErrorContainer, exportFormatCheckboxes) {
        this.bboxFields = bboxFields;
        this.excerptBoundsErrorContainer = excerptBoundsErrorContainer;
        this.exportFormatCheckboxes = exportFormatCheckboxes;

        this.validateFormatCheckboxes = function() {
            var validity = window.objectToArray(this.exportFormatCheckboxes).some(function(checkbox){
                return checkbox.checked;
            });
            window.objectToArray(this.exportFormatCheckboxes).forEach(function(checkbox){
                var validityMessage = validity ? '' : 'Please select at least one format!';
                checkbox.setCustomValidity(validityMessage);
            }, this);
        }.bind(this);

        this.areAllBoxesSet = function(){
            return this.bboxFields.north.value &&
                this.bboxFields.east.value &&
                this.bboxFields.south.value &&
                this.bboxFields.west.value
        }.bind(this);

        this.validateExcerptBoundInputFields = function() {
            var allowedMaxSize = 250 * 1024 * 1024;
            if (this.areAllBoxesSet()) {

                jQuery.getJSON(
                    '/api/estimated_file_size/',
                    {
                        'north': this.bboxFields.north.value,
                        'east': this.bboxFields.east.value,
                        'south': this.bboxFields.south.value,
                        'west': this.bboxFields.west.value
                    },
                    function (data) {
                        var estimatedFileSize = Number(data['estimated_file_size_in_bytes']);
                        var validity = estimatedFileSize < allowedMaxSize;

                        window.objectToArray(this.bboxFields).forEach(function (bboxField) {
                            if (validity) {
                                bboxField.setCustomValidity('');
                                this.excerptBoundsErrorContainer.textContent = '';
                            } else {
                                var howMuchTooLarge = estimatedFileSize ? Math.ceil(estimatedFileSize * 100 / allowedMaxSize - 100) + '% ' : '';
                                var message = 'Excerpt {percent}too large!'.replace('{percent}', howMuchTooLarge);
                                bboxField.setCustomValidity(message);
                                this.excerptBoundsErrorContainer.textContent = message;
                            }
                        }.bind(this));
                    }.bind(this)
                );
            }
        }.bind(this);

        this.validate = function() {
            this.validateExcerptBoundInputFields();
            this.validateFormatCheckboxes();
        }.bind(this);
    };


    window.addEventListener('load', function() {
        if(document.getElementById('newExcerptForm')) {
            var bboxFields = {
                north: document.getElementById('id_north'),
                east: document.getElementById('id_east'),
                west: document.getElementById('id_west'),
                south: document.getElementById('id_south')
            };
            var bboxErrorField = document.getElementById('bounding-box-error');
            var exportFormatCheckboxes = document.querySelectorAll('#div_id_formats input[type="checkbox"]');

            var formValidator = new FormValidator(bboxFields, bboxErrorField, exportFormatCheckboxes);

            window.objectToArray(bboxFields).forEach(function(bboxField){
                window.addEventMultipleListeners(bboxField, ['valueUpdate', 'change', 'input', 'paste'], formValidator.validate);
            });
            window.objectToArray(exportFormatCheckboxes).forEach(function(checkBox){
                checkBox.addEventListener('change', formValidator.validate);
            });

            formValidator.validate();
        }
    });
})();
