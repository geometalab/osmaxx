(function() {
    this.deactivateAllParts = function(formPartNodes) {
        Array.prototype.forEach.call(formPartNodes,function(node) {
            node.setAttribute('data-form-part-state', 'inactive');
        });
    };

    this.activateSelectedPart = function(form, formPartsSwitcher, formPartsButtons) {
        var formPartId = (formPartsButtons.item(formPartsSwitcher.selectedIndex)).getAttribute('data-form-part-for');
        form.querySelector('[data-form-part="'+formPartId+'"]').setAttribute('data-form-part-state', 'active');
        if(window.location.hash.substring(1) != formPartId) {
            window.history.pushState({ formPartId: formPartId }, '', '#'+formPartId);
        }
    };

    this.initializeFormModes = function(form, formPartsSwitcher, formPartsButtons, formPartNodes, activeFormPartId) {
        var formModeParam = window.location.hash.substring(1);

        // no param given -> update param to id of first form part (the current active form part)
        if(formModeParam == '') {
            window.history.replaceState({ formPartId: activeFormPartId }, '', '#'+activeFormPartId);
        }

        // param of inactive form part given -> change to parts
        if(formModeParam != '' && formModeParam != activeFormPartId) {
            formPartsSwitcher.value = formModeParam;
        }

        formPartsSwitcher.dispatchEvent(new Event('change'));
    }

    window.addEventListener('load', function() {
        var formPartNodes = document.querySelectorAll('[data-form-part]');
        var form = formPartNodes.item(0).parentNode;
        var formPartsSwitcher = document.querySelector('select[data-form-part-switcher]');
        var formPartsButtons = document.querySelectorAll('[data-form-part-for]');

        formPartsSwitcher.addEventListener('change',function(event) {
            deactivateAllParts(formPartNodes);
            activateSelectedPart(form, formPartsSwitcher, formPartsButtons);
        });

        window.onpopstate = function(event) {
            // if pushState tries to push the current location, there will be no history entry -> event.state is undefined
            var formPartId = (event.state) ? event.state.formPartId : window.location.hash;
            var currentButton = document.querySelector('[data-form-part-for="'+formPartId+'"]');

            if(formPartsSwitcher.value != formPartId) {
                formPartsSwitcher.value = formPartId;
                formPartsSwitcher.dispatchEvent(new Event('change'));
            }
        };

        var currentActiveFormPart = document.querySelector('[data-form-part-state="active"]');
        var activeFormPartId = (currentActiveFormPart) ? currentActiveFormPart.getAttribute('data-form-part-for') :
            document.querySelector('[data-form-part]').getAttribute('data-form-part');
        initializeFormModes(form, formPartsSwitcher, formPartsButtons, formPartNodes, activeFormPartId );
    });
})();
