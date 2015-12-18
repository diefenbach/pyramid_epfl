epfl.Checkbox = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Checkbox.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Checkbox.prototype, 'input_selector', {
    get: function() {
        return "#" + this.cid + "_input";
    }
});

epfl.Checkbox.prototype.custom_handle_change = function(event) {
    // custom handler needed, cause the value is not just $elm.val()
    var value =  $(this.input_selector).is(':checked');
    this.handle_change(event, value);
};

epfl.Checkbox.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    $(this.input_selector).attr('checked', $(this.input_selector).val() == 'True');

    $(this.input_selector)
        .blur(this.custom_handle_change.bind(this))
        .change(this.custom_handle_change.bind(this));
};
