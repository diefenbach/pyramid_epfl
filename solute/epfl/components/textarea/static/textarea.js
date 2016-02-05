epfl.Textarea = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Textarea.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Textarea.prototype, 'form_element', {
    get: function() {
        return $("#" + this.cid + "_input");
    }
});

epfl.Textarea.prototype.handle_keypress = function(event) {
    if(this.params.max_length) {
        $("#" + this.cid + '_input' + '_count').text(this.form_element.val().length);
    }
};


epfl.Textarea.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.register_change_handler();

    var compo = this;
    if (compo.params.show_count) {
        compo.elm.keyup(compo.handle_keypress.bind(compo));
    }
};
