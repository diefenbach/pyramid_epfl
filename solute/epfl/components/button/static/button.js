epfl.Button = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Button.inherits_from(epfl.ComponentBase);

epfl.Button.prototype.handle_click = function(event) {
    // No super since handle_local_click is not required here

    if (this.params.stop_propagation_on_click) {
        event.stopPropagation();
    }

    var button_elm = $('#' + this.cid);
    if (button_elm.hasClass("disabled")) {
        return;
    }

    if (this.params["confirm_first"] && (!confirm(this.params["confirm_message"]))) {
        return;
    }
    if (this.params["disable_on_click"]) {
        button_elm.addClass("disabled");
    }
    if(this.params["event_target"]) {
        epfl.send(epfl.make_component_event(this.params["event_target"], this.params["event_name"]));
        return;
    }
    this.send_event(this.params["event_name"], {});
};
