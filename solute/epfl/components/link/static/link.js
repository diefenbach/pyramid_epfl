epfl.Link = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Link.inherits_from(epfl.ComponentBase);

epfl.Link.prototype.ContextMenu = function () {
    var element = $("[epflid='" + this.cid + "'] ul.context-dropdown-menu");
    var that = this;

    element.parent().mouseleave(function (event) {
        element.hide();
    });

    element.children("li.entry").click(function (event) {
        event.stopPropagation();
        $(this).parent().hide();
        var liEvent = $(this).data("event");
        var liId = $(this).data("id");
        var liData = $(this).data("data");
        that.send_event(liEvent, {entry_id: liId, data: liData});
    });

    element.parent().find("button").click(function (event) {
        event.stopPropagation();
        var ul = $(this).parent().find("ul");
        if (ul.is(":visible")) {
            ul.hide();
        } else {
            ul.show();
            ul.css({
                top: ($(this).offset().top + $(this).height() + 3) - $(window).scrollTop(),
                left: $(this).offset().left - (ul.width() - $(this).width() - 10)
            })
        }
    });

    $(document).click(function(){
        $("ul.context-dropdown-menu").hide();
    });
};

epfl.Link.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    this.ContextMenu();
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
