epfl.Select = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Select.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Select.prototype, 'form_element', {
    get: function () {
        return $("#" + this.cid + " select");
    }
});

epfl.Select.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.register_change_handler();
    this.register_submit_form_on_enter_handler();
};
