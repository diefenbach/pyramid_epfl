epfl.SimpleToggle = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.SimpleToggle.inherits_from(epfl.FormInputBase);

epfl.SimpleToggle.prototype.handle_click = function (event) {
    epfl.FormInputBase.prototype.handle_click.call(this, event);

    var target = $(event.target);
    var obj = this;

    if (target.attr('id') == this.cid + "_button" || target.parent().attr('id') == this.cid + "_button") {
        event.stopImmediatePropagation();
        event.preventDefault();
        event.stopPropagation();
        var input_field = obj.elm.find('input');
        var old_value = input_field.val();
        var val = "True";
        if (old_value == "True") {
            val = "False";
        }
        input_field.val(val);
        var toggle_value = (val == "True");
        obj.elm.
            find("i").
            toggleClass("fa-" + obj.params["disabled_icon"]).
            toggleClass("fa-" + obj.params["disabled_icon_size"]).
            toggleClass("text-" + obj.params["disabled_icon_color"]).
            toggleClass("fa-" + obj.params["enabled_icon"]).
            toggleClass("fa-" + obj.params["enabled_icon_size"]).
            toggleClass("text-" + obj.params["enabled_icon_color"]);

        this.handle_change(event, toggle_value);
    }
};
