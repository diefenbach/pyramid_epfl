epfl.ContextListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var obj = this;
    epfl.ContextListLayout.ContextEvent = function (event, param) {
        obj.send_event(cid, event, param);
    };

    epfl.PluginContextMenu("#" + cid + " ul.context-dropdown-menu",cid);
};

epfl.ContextListLayout.inherits_from(epfl.ComponentBase);
