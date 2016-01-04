epfl.Toggle = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Toggle.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Toggle.prototype, 'form_element', {
    'get': function() {
        return $("#" + this.cid + "_input");
    }
});

epfl.Toggle.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    // control the gui
    this.form_element.attr('checked', this.form_element.val() == 'True');
    this.form_element.bootstrapSwitch('state');

    // wrap bootstrap event to handle_change
    var compo = this;
    this.form_element.on('switchChange.bootstrapSwitch', function(event) {
        var val = compo.elm.find('.bootstrap-switch').hasClass('bootstrap-switch-on');
        compo.handle_change(event, val);
    });
};
