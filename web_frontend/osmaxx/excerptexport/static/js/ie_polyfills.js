(function () {
    var customEventSupportsNewKeyword = function() {
        try {
            new CustomEvent('it-supports-custom-events');
            return true;
        } catch (e) {
            return false;
        }
    };

    if (!customEventSupportsNewKeyword()) {
        function CustomEvent ( event, params ) {
            params = params || { bubbles: false, cancelable: false, detail: undefined };
            var evt = document.createEvent( 'CustomEvent' );
            evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
            return evt;
        }
        CustomEvent.prototype = window.Event.prototype;
        window.CustomEvent = CustomEvent;
    }
})();
