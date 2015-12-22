epfl.Textarea = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Textarea.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Textarea.prototype, 'elm_input', {
    get: function() {
        return $("#" + this.cid + "_input");
    }
});

epfl.Textarea.prototype.handle_change = function(event) {
    var enqueue_event = !this.params.fire_change_immediately;
    epfl.FormInputBase.on_change(this, this.elm_input.val(), this.cid, enqueue_event);
};

epfl.Textarea.prototype.after_response = function(data) {
    this.elm_input.blur(this.handle_change.bind(this)).change(this.handle_change.bind(this));
};
