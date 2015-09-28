epfl.Link = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Link.inherits_from(epfl.ComponentBase);

epfl.Link.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);
    if (this.params.event_name) {
        this.send_event(this.params.event_name);
        event.originalEvent.preventDefault();
    }
    if (this.params.stop_propagration_on_click) {
        event.stopPropagation();
    }
};

epfl.Link.prototype.handle_double_click = function (event) {
    epfl.ComponentBase.prototype.handle_double_click.call(this, event);
    if (this.params.double_click_event_name) {
        this.send_event(this.params.double_click_event_name);
        event.originalEvent.preventDefault();
    }
    if (this.params.stop_propagration_on_click) {
        event.stopPropagation();
    }
};
