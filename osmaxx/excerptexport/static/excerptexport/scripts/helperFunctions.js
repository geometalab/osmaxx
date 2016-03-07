window.objectToArray = function(nodeList) {
    return Object.keys(nodeList).map(function(index) {
        return nodeList[index];
    });
};

window.addEventMultipleListeners = function(node, eventNames, listener) {
    eventNames.forEach(function(eventName) {
        node.addEventListener(eventName, listener);
    });
};
