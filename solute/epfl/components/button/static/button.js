epfl.Button = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Button.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Button.prototype, 'button', {
    get: function () {
        return $('#' + this.cid);
    }
});

epfl.Button.prototype.after_response = function(data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);

    // make sure we have a proper event_target
    if (!this.params['event_target']) {
        this.params['event_target'] = this.cid;
    }
};

epfl.Button.prototype.handle_click = function(event) {
    // No super since handle_local_click is not required here
    if (this.params.stop_propagation_on_click) {
        event.stopPropagation();
    }

    if (this.button.hasClass("disabled")) {
        return;
    }

    if (this.params["disable_on_click"]) {
        this.button.addClass("disabled");
    }

    if (this.params["confirm_first"] && (!confirm(this.params["confirm_message"]))) {
        return;
    }

    epfl.send(epfl.make_component_event(this.params["event_target"],
                                        this.params["event_name"]));
};
