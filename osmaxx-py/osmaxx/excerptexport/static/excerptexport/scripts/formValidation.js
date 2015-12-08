'use strict';

(function() {
    var FormValidator = function() {
        this.submitButton = document.getElementById('submit-id-submit');
        this.extractionFormatCheckboxes = document.querySelectorAll('#div_id_formats input[type="checkbox"]');
        this.excerptBoundInputFields = [
            document.getElementById('id_north'),
            document.getElementById('id_east'),
            document.getElementById('id_south'),
            document.getElementById('id_west')
        ];

        this.validity = {
            'extractionFormats': false,
            'excerptBounds': false
        };

        this.isFormValid = function() {
            var isValid = true;
            Object.keys(this.validity).forEach(function(key){
                isValid = isValid && this.validity[key];
            }.bind(this));
            return isValid;
        };

        this.setSubmitButtonState = function(overrideState) {
            if(overrideState == undefined) {
                this.submitButton.disabled = !this.isFormValid();
            } else {
                this.submitButton.disabled = !overrideState;
            }
        }

        this.validateExtractionFormatCheckboxes = function() {
            this.validity['extractionFormats'] = (document.querySelectorAll('#div_id_formats input[type="checkbox"]:checked').length > 0);
            this.setSubmitButtonState();
            Array.prototype.forEach.call(this.extractionFormatCheckboxes, function(checkbox) {
                if(this.validity['extractionFormats']) {
                    checkbox.setCustomValidity('');
                } else {
                    checkbox.setCustomValidity('Please choose minimal one export format!');
                }
            }.bind(this));
            this.setSubmitButtonState();
        }.bind(this);

        this.validateExcerptBounds = function() {
            var allowedMaxSize = 500*1024*1024; // 500 MB

            var north = document.getElementById('id_north').value;
            var east = document.getElementById('id_east').value;
            var south = document.getElementById('id_south').value;
            var west = document.getElementById('id_west').value;

            jQuery.getJSON(
                '/api/estimated_file_size/',
                { 'north': north, 'east': east, 'south': south, 'west': west },
                function(data) {
                    var estimatedFileSize = Number(data['estimated_file_size_in_bytes']);
                    if(estimatedFileSize) {
                        document.querySelector('#file-size').textContent = 'Estimated file size: ∼'+Math.ceil(estimatedFileSize/1024/1024)+' MB.';
                    }
                    this.validity['excerptBounds'] = estimatedFileSize < allowedMaxSize;
                    this.setSubmitButtonState();
                    
                    this.excerptBoundInputFields.forEach(function(excerptBoundInputField) {
                        if(this.validity['excerptBounds']) {
                            excerptBoundInputField.setCustomValidity('');
                            document.getElementById('excerpt-validation').textContent = '';
                        } else {
                            var message = 'Excerpt too large'+(estimatedFileSize ? ' (∼'+Math.ceil(estimatedFileSize/1024/1024)+' MB)' : '')+'!';
                            excerptBoundInputField.setCustomValidity(message);
                            document.getElementById('excerpt-validation').textContent = 'Excerpt too large!';
                        }
                    }.bind(this));
                }.bind(this)
            );
        }.bind(this);


        Array.prototype.forEach.call(this.extractionFormatCheckboxes, function(formatCheckbox) {
            formatCheckbox.addEventListener('change', this.validateExtractionFormatCheckboxes);
        }.bind(this));

        this.excerptBoundInputFields.forEach(function(excerptBoundsInputField) {
            excerptBoundsInputField.addEventListener('valueUpdate', this.validateExcerptBounds);
        }.bind(this));

        this.setSubmitButtonState(false);
        this.validateExtractionFormatCheckboxes();
        this.validateExcerptBounds();
    };

    window.addEventListener('load', function(){
        if(document.getElementById('extractionOrderForm')) {
            var validator = new FormValidator();
        };
    });
})();
