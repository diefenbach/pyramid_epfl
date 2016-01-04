epfl.ButtonRadio = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.ButtonRadio.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.ButtonRadio.prototype, 'form_element', {
    'get': function() {
        return $("input[type=radio][name=" + this.cid + "]");
    }
});

epfl.ButtonRadio.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.register_change_handler();
};
