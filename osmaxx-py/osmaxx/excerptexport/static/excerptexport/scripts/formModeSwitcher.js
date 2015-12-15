(function() {
    var FormPartManager = function() {
        this.formPartNodes = document.querySelectorAll('[data-form-part]');
        this.form = this.formPartNodes.item(0).parentNode;
        this.formPartsSwitcher = document.querySelector('select[data-form-part-switcher]');
        this.formPartsButtons = document.querySelectorAll('[data-form-part-for]');


        this.deactivateAllParts = function() {
            Array.prototype.forEach.call(this.formPartNodes, function(node) {
                node.setAttribute('data-form-part-state', 'inactive');
            });
        };

        this.activateSelectedPart = function() {
            var formPartId = (this.formPartsButtons.item(this.formPartsSwitcher.selectedIndex)).getAttribute('data-form-part-for');
            this.form.querySelector('[data-form-part="'+formPartId+'"]').setAttribute('data-form-part-state', 'active');
            if(window.location.hash.substring(1) != formPartId) {
                window.history.pushState({ formPartId: formPartId }, '', '#'+formPartId);
            }
        };

        this.initializeFormModes = function() {
            var currentActiveFormPart = document.querySelector('[data-form-part-state="active"]');
            var activeFormPartId = (currentActiveFormPart) ? currentActiveFormPart.getAttribute('data-form-part-for') :
                document.querySelector('[data-form-part]').getAttribute('data-form-part');

            var formModeParam = window.location.hash.substring(1);

            // no param given -> update param to id of first form part (the current active form part)
            if(formModeParam == '') {
                window.history.replaceState({ formPartId: activeFormPartId }, '', '#'+activeFormPartId);
            }

            // param of inactive form part given -> change to parts
            if(formModeParam != '' && formModeParam != activeFormPartId) {
                this.formPartsSwitcher.value = formModeParam;
                this.formPartsSwitcher.dispatchEvent(new Event('valueUpdate'));
            }

            this.onFormPartsSwitcherChange();
        };

        this.onFormPartsSwitcherChange = function() {
            this.deactivateAllParts();
            this.activateSelectedPart();
        }.bind(this);


        // constructor
        this.formPartsSwitcher.addEventListener('change', this.onFormPartsSwitcherChange);

        window.onpopstate = function(event) {
            // if pushState tries to push the current location, there will be no history entry -> event.state is undefined
            var formPartId = (event.state) ? event.state.formPartId : window.location.hash;
            var currentButton = document.querySelector('[data-form-part-for="'+formPartId+'"]');

            if(this.formPartsSwitcher.value != formPartId) {
                this.formPartsSwitcher.value = formPartId;
                this.formPartsSwitcher.dispatchEvent(new Event('valueUpdate'));
                this.onFormPartsSwitcherChange();
            }
        }.bind(this);

        this.initializeFormModes();
    };


    window.addEventListener('load', function() {
        window.formPartManager = new FormPartManager();
    });
})();
