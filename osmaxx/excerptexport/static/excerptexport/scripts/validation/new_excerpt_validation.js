(function() {
    /**
     * Uses html5 setCustomValidity()
     * The browser will disable the submit button by it's own if some element contains an error message set by setCustomValidity()
     */
    var FormValidator = function (exportFormatCheckboxes) {
        this.exportFormatCheckboxes = exportFormatCheckboxes;
        this.validateFormatCheckboxes = function () {
            var validity = window.objectToArray(this.exportFormatCheckboxes).some(function (checkbox) {
                return checkbox.checked;
            });
            window.objectToArray(this.exportFormatCheckboxes).forEach(function (checkbox) {
                var validityMessage = validity ? '' : 'Please select at least one format!';
                checkbox.setCustomValidity(validityMessage);
            }, this);
        }.bind(this);

        this.validate = function () {
            this.validateFormatCheckboxes();
        }.bind(this);
    };

    window.addEventListener('load', function () {
        if (document.getElementById('newExcerptForm')) {
            var exportFormatCheckboxes = document.querySelectorAll('#div_id_formats input[type="checkbox"]');
            var formValidator = new FormValidator(exportFormatCheckboxes);

            window.objectToArray(exportFormatCheckboxes).forEach(function (checkBox) {
                checkBox.addEventListener('change', formValidator.validate);
            });

            formValidator.validate();
        }
    });
})();
