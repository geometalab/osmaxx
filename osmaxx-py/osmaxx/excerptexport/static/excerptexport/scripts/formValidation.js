'use strict';

(function() {
    // TODO: get strings from translation helper
    var FormValidator = function() {
        this.submitButton = document.getElementById('submit-id-submit');
        this.extractionFormatCheckboxes = document.querySelectorAll('#div_id_formats input[type="checkbox"]');
        this.excerptBoundInputFields = [
            document.getElementById('id_north'),
            document.getElementById('id_east'),
            document.getElementById('id_south'),
            document.getElementById('id_west')
        ];
        this.formModeSwitcher = document.getElementById('id_form_mode');
        this.existingExcerptSelect = document.getElementById('id_existing_excerpts');
        this.newExcerptName = document.getElementById('id_name');

        this.validity = {
            'extractionFormats': false,
            'excerptBounds': false,
            'existingExcerptOrNew': false
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


        this.validateExistingExcerptOrNew = function() {
            if(this.formModeSwitcher.value == "existing-excerpt") {
                var selectValue = this.existingExcerptSelect.value;
                if (!isNaN(parseFloat(selectValue)) && parseFloat(selectValue) > 0) {
                    this.validity['existingExcerptOrNew'] = true;
                } else {
                    this.validity['existingExcerptOrNew'] = false;
                }
            } else if(this.formModeSwitcher.value == "new-excerpt") {
                if(this.newExcerptName.value.length > 2) {
                    this.validity['existingExcerptOrNew'] = true;
                } else {
                    this.validity['existingExcerptOrNew'] = false;
                }
            }
            this.setSubmitButtonState();
        }.bind(this);

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
            var allowedMaxSize = 250*1024*1024;

            var north = document.getElementById('id_north').value;
            var east = document.getElementById('id_east').value;
            var south = document.getElementById('id_south').value;
            var west = document.getElementById('id_west').value;

            jQuery.getJSON(
                '/api/estimated_file_size/',
                { 'north': north, 'east': east, 'south': south, 'west': west },
                function(data) {
                    var estimatedFileSize = Number(data['estimated_file_size_in_bytes']);
                    this.validity['excerptBounds'] = estimatedFileSize < allowedMaxSize;
                    this.setSubmitButtonState();
                    
                    this.excerptBoundInputFields.forEach(function(excerptBoundInputField) {
                        if(this.validity['excerptBounds']) {
                            excerptBoundInputField.setCustomValidity('');
                            document.getElementById('excerpt-validation').textContent = '';
                        } else {
                            var howMuchToLarge = estimatedFileSize ? Math.ceil(estimatedFileSize*100/allowedMaxSize-100) + '% ': '';
                            var message = 'Excerpt {percent}too large!'.replace('{percent}', howMuchToLarge);
                            excerptBoundInputField.setCustomValidity(message);
                            document.getElementById('excerpt-validation').textContent = message;
                        }
                    }.bind(this));
                }.bind(this)
            );
        }.bind(this);

        // watch elements
        Array.prototype.forEach.call(this.extractionFormatCheckboxes, function(formatCheckbox) {
            formatCheckbox.addEventListener('change', this.validateExtractionFormatCheckboxes);
        }.bind(this));

        this.excerptBoundInputFields.forEach(function(excerptBoundsInputField) {
            excerptBoundsInputField.addEventListener('valueUpdate', this.validateExcerptBounds);
        }.bind(this));

        this.formModeSwitcher.addEventListener('change', this.validateExistingExcerptOrNew);
        this.existingExcerptSelect.addEventListener('change', this.validateExistingExcerptOrNew);
        this.newExcerptName.addEventListener('change', this.validateExistingExcerptOrNew);
        this.newExcerptName.addEventListener('input', this.validateExistingExcerptOrNew);
        this.newExcerptName.addEventListener('paste', this.validateExistingExcerptOrNew);

        // initial state
        this.setSubmitButtonState(false);
        this.validateExistingExcerptOrNew();
        this.validateExtractionFormatCheckboxes();
        this.validateExcerptBounds();
    };

    window.addEventListener('load', function(){
        if(document.getElementById('extractionOrderForm')) {
            var validator = new FormValidator();
        };
    });
})();
