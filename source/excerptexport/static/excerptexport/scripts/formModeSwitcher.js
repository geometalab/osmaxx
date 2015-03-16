(function() {
    this.deactivateAllParts = function(formPartNodes) {
        [].forEach.call(formPartNodes,function(node) {
            node.setAttribute('data-form-part-state', 'inactive');
        });
    };

    this.activateSelectedPart = function(form, formPartsSwitcher, formPartsButtons) {
        var formPartId = (formPartsButtons.item(formPartsSwitcher.selectedIndex)).getAttribute('data-form-part-for');
        form.querySelector('[data-form-part="'+formPartId+'"]').setAttribute('data-form-part-state', 'active');
    }

    window.addEventListener('load', function() {
        var formPartNodes = document.querySelectorAll('[data-form-part]');
        var form = formPartNodes.item(0).parentNode;
        var formPartsSwitchers = document.querySelectorAll('select[data-form-part-switcher]');
        var formPartsButtons = document.querySelectorAll('[data-form-part-for]');

        deactivateAllParts(formPartNodes);

        [].forEach.call(formPartsSwitchers,function(node) {
            node.addEventListener('change',function(event) {
                deactivateAllParts(formPartNodes);
                activateSelectedPart(form, node, formPartsButtons);
            })

            activateSelectedPart(form, node, formPartsButtons);
        });
    });
})();