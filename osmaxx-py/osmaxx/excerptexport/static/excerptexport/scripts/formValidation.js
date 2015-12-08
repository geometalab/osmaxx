'use strict';

(function() {
    var FormValidator = function() {
        this.submitButton = document.getElementById('submit-id-submit');
        this.extractionFormatCheckboxes = document.querySelectorAll('#div_id_formats input[type="checkbox"]');


        this.validity = {
            'extractionFormats': false
        };

        this.isFormValid = function() {
            return Object.keys(this.validity).every(function(key){
                return this.validity[key];
            }, this);
        };

        this.setSubmitButtonState = function() {
            this.submitButton.disabled = !this.isFormValid();
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
        }.bind(this);


        Array.prototype.forEach.call(this.extractionFormatCheckboxes, function(formatCheckbox) {
            formatCheckbox.addEventListener('change', this.validateExtractionFormatCheckboxes);
        }.bind(this));

        this.validateExtractionFormatCheckboxes();
        this.setSubmitButtonState();
    };

    window.addEventListener('load', function(){
        if(document.getElementById('extractionOrderForm')) {
            var validator = new FormValidator();
        };
    });
})();
