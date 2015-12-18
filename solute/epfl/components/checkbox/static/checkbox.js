epfl.Checkbox = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Checkbox.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Checkbox.prototype, 'input_selector', {
    get: function() {
        return "#" + this.cid + "_input";
    }
});

epfl.Checkbox.prototype.handle_change = function(event) {
    var enqueue_event = !this.params.fire_change_immediately;
    epfl.FormInputBase.on_change(this, $(this.input_selector).is(':checked'), this.cid, enqueue_event);
};

epfl.Checkbox.prototype.after_response = function() {
    $(this.input_selector).attr('checked', $(this.input_selector).val() == 'True');
    $(this.input_selector).blur(this.handle_change.bind(this)).change(this.handle_change.bind(this));
};
