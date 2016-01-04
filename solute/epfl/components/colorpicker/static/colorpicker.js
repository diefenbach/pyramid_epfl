epfl.ColorPicker = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};
epfl.ColorPicker.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.ColorPicker.prototype, 'specialfield', {
    get: function () {
        return this.elm.find('div.epfl-colorpicker-specialfield');
    }
});

Object.defineProperty(epfl.ColorPicker.prototype, 'colorfield', {
    get: function () {
        return this.elm.find('div.epfl-colorpicker-colorfield');
    }
});

Object.defineProperty(epfl.ColorPicker.prototype, 'colorfield_icon', {
    get: function () {
        return this.elm.children('div').find('i.fa');
    }
});

Object.defineProperty(epfl.ColorPicker.prototype, 'toggle_button', {
    get: function () {
        return this.elm.find('button');
    }
});

Object.defineProperty(epfl.ColorPicker.prototype, 'toggle_button_icon', {
    get: function () {
        return this.elm.find('button').children("i");
    }
});

epfl.ColorPicker.prototype.closeOnOutsideClick = function (event) {
    if ($(event.target.closest("[epflid]")).attr("epflid") !== this.cid && this.params["colors_visible"]) {
        this.send_event("toggle", {});
    }
    $(document).unbind(event);
};

epfl.ColorPicker.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    $("div.tooltip.fade.top.in").remove(); //Bugfix for hiding tooltips after redraw
    this.elm.find('[data-toggle="tooltip"]').tooltip();
    $(document).bind("click", this.closeOnOutsideClick.bind(this));
};

epfl.ColorPicker.prototype.handle_local_click = function (event) {
    epfl.FormInputBase.prototype.handle_local_click.call(this, event);
    var value = null;
    var target = $(event.target);
    if (this.specialfield.is(event.target) || this.colorfield.is(event.target)) {
        value = target.data("value");
    } else if (this.colorfield_icon.is(event.target)) {
        value = target.parent().data("value");
    } else if (this.toggle_button.is(event.target) || this.toggle_button_icon.is(event.target)) {
        this.send_event("toggle", {});
    }

    if (value !== null) {
        this.send_event("change", {"value": value});
    }
};
