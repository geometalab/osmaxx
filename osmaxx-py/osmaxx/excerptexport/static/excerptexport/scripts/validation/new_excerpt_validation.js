(function(){
    var FormValidator = function(nameField, bboxFields, excerptBoundsErrorContainer, submitButton) {
        this.nameField = nameField;
        this.bboxFields = bboxFields;
        this.excerptBoundsErrorContainer = excerptBoundsErrorContainer;
        this.submitButton = submitButton;

        this.validity = {
            excerptBounds: false,
            excerptName: false
        };

        this.checkNameField = function() {
            this.validity['excerptName'] = this.nameField.value.length >= 2;
            if(this.validity['excerptName']) {
                this.nameField.setCustomValidity('');
            } else {
                this.nameField.setCustomValidity('Please enter a valid name!');
            }
        }.bind(this);

        this.checkExcerptBounds = function() {
            var allowedMaxSize = 250 * 1024 * 1024;

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
                    this.validity['excerptBounds'] = estimatedFileSize < allowedMaxSize;
                    this.setSubmitButtonState();

                    Object.keys(this.bboxFields).forEach(function (index) {
                        var excerptBoundInputField = this.bboxFields[index];
                        if (this.validity['excerptBounds']) {
                            excerptBoundInputField.setCustomValidity('');
                            this.excerptBoundsErrorContainer.textContent = '';
                        } else {
                            var howMuchTooLarge = estimatedFileSize ? Math.ceil(estimatedFileSize * 100 / allowedMaxSize - 100) + '% ' : '';
                            var message = 'Excerpt {percent}too large!'.replace('{percent}', howMuchTooLarge);
                            excerptBoundInputField.setCustomValidity(message);
                            this.excerptBoundsErrorContainer.textContent = message;
                        }
                    }.bind(this));
                }.bind(this)
            );
        }.bind(this);

        this.isFormValid = function() {
            return Object.keys(this.validity).every(function(key){
                return this.validity[key];
            }, this);
        };

        this.setSubmitButtonState = function(overrideState) {
            if(overrideState == undefined) {
                this.submitButton.disabled = !this.isFormValid();
            } else {
                this.submitButton.disabled = !overrideState;
            }
        };

        this.validate = function() {
            this.checkNameField();
            this.checkExcerptBounds();
            this.setSubmitButtonState();
        }.bind(this);
    };

    window.addEventListener('load', function() {
        if(document.getElementById('newExcerptForm')) {
            var nameField = document.getElementById('id_name');
            var bboxFields = {
                north: document.getElementById('id_north'),
                east: document.getElementById('id_east'),
                west: document.getElementById('id_west'),
                south: document.getElementById('id_south'),
            };
            var bboxErrorField = document.getElementById('bounding-box-error');
            var submitButton = document.getElementById('submit-id-submit');

            var formValidator = new FormValidator(nameField, bboxFields, bboxErrorField, submitButton);

            nameField.addEventListener('change', formValidator.validate);
            nameField.addEventListener('input', formValidator.validate);
            nameField.addEventListener('paste', formValidator.validate);

            Object.keys(bboxFields).forEach(function(index){
                bboxFields[index].addEventListener('valueUpdate', formValidator.validate);
                bboxFields[index].addEventListener('input', formValidator.validate);
                bboxFields[index].addEventListener('paste', formValidator.validate);
            });

            formValidator.validate();
        }
    });
})();
