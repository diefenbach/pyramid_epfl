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

    obj.context_menu_entry.click(function (event) {
        event.stopPropagation();
        obj.context_menu.hide();
        obj.send_event($(this).data("event"), {});
    });

    obj.context_menu_button.click(function (event) {
        event.stopPropagation();
        if (obj.context_menu.is(":visible")) {
            obj.context_menu.hide();
        } else {
            obj.context_menu.show();
            obj.context_menu.css({
                top: ($(this).offset().top + $(this).height() + 3) - $(window).scrollTop(),
                left: $(this).offset().left - (obj.context_menu.width() - $(this).width() - 10)
            })
        }
    });

    $(document).click(function () {
        obj.context_menu.hide();
    });
};

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
