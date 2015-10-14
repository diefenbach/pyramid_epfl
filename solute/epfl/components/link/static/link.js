epfl.Link = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Link.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Link.prototype, 'context_menu', {
    get: function () {
        return this.elm.children('ul.context-dropdown-menu');
    }
});

Object.defineProperty(epfl.Link.prototype, 'context_menu_button', {
    get: function () {
        return this.elm.children('button');
    }
});

Object.defineProperty(epfl.Link.prototype, 'context_menu_button_icon', {
    get: function () {
        return this.context_menu_button.children("i");
    }
});

Object.defineProperty(epfl.Link.prototype, 'context_menu_entry', {
    get: function () {
        return this.context_menu.children('li.entry');
    }
});

epfl.Link.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    var obj = this;

    obj.elm.mouseleave(function (event) {
        obj.context_menu.hide();
    });
};

epfl.Link.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);

    if (this.params.event_name) {
        this.send_event(this.params.event_name);
        event.originalEvent.preventDefault();
    }
    if (this.params.stop_propagation_on_click) {
        event.stopPropagation();
    }

    if (this.context_menu_button.is(event.target) || this.context_menu_button_icon.is(event.target)) {
        if (this.context_menu.is(":visible")) {
            this.context_menu.hide();
        } else {
            this.context_menu.show();
            this.context_menu.css({
                top: (this.context_menu_button.offset().top + this.context_menu_button.height() + 3) - $(window).scrollTop(),
                left: this.context_menu_button.offset().left - (this.context_menu.width() - this.context_menu_button.width() - 10)
            });
        }
    } else if (this.context_menu_entry.is(event.target)) {
        this.context_menu.hide();
        this.send_event($(event.target).data("event"), {});
    } else if (this.params.popover_text) {
        this.elm.popover('toggle');
    }

};

epfl.Link.prototype.handle_double_click = function (event) {
    epfl.ComponentBase.prototype.handle_double_click.call(this, event);
    if (this.params.double_click_event_name) {
        this.send_event(this.params.double_click_event_name);
        event.originalEvent.preventDefault();
    }
    if (this.params.stop_propagation_on_click) {
        event.stopPropagation();
    }
};

epfl.Link.prototype.handle_shift_click = function (event) {
    epfl.ComponentBase.prototype.handle_shift_click.call(this, event);
    if (this.params.shift_click_event_name) {
        this.send_event(this.params.shift_click_event_name);
        event.preventDefault();
        event.originalEvent.preventDefault();
    }
    if (this.params.stop_propagation_on_click) {
        event.stopPropagation();
    }
};
