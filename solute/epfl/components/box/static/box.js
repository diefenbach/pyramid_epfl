epfl.Box = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Box.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Box.prototype, 'close_icon', {
    get: function () {
        return this.elm.find('#close_' + this.cid);
    }
});

Object.defineProperty(epfl.Box.prototype, 'refresh_icon', {
    get: function () {
        return this.elm.find('#refresh_' + this.cid);
    }
});

epfl.Box.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);

    if ((this.elm.is(event.target) && this.params.hover_box) || (this.close_icon.is(event.target))) {
        // click on close button or outside of box
        if (!this.params.hover_box_remove_on_close && this.params.hover_box) {
            this.send_event("hide", {});
        } else {
            this.send_event("removed", {});
        }
        event.stopImmediatePropagation();
        event.preventDefault();
    }
    else if (this.refresh_icon.is(event.target)) {
        this.send_event("reinitialize", {});
        event.stopImmediatePropagation();
        event.preventDefault();
    }

};
