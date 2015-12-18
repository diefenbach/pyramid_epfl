epfl.Radio = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Radio.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Radio.prototype, 'input_selector', {
    'get': function() {
        return "#" + this.cid + " input[name=" + this.cid + "]";
    }
});

epfl.Radio.prototype.handle_change = function(event) {
    var enqueue_event = !this.params.fire_change_immediately;
    epfl.FormInputBase.on_change(this, $(event.target).val(), this.cid, enqueue_event);
};

epfl.Radio.prototype.after_response = function(data) {
    $(this.input_selector).change(this.handle_change.bind(this));
};
