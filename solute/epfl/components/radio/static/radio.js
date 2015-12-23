epfl.Radio = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Radio.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Radio.prototype, 'form_element', {
    'get': function() {
        return $("#" + this.cid + " input[name=" + this.cid + "]");
    }
});

epfl.Radio.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.register_change_handler();
};
