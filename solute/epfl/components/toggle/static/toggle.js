epfl.Toggle = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.Toggle.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.Toggle.prototype, 'input_selector', {
    'get': function() {
        return "#" + this.cid + "_input";
    }
});

epfl.Toggle.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    // control the gui
    $(this.input_selector).attr('checked', $(this.input_selector).val() == 'True');
    $(this.input_selector).bootstrapSwitch('state');

    // wrap bootstrap wevent to handle_change
    var compo = this;
    $(this.input_selector).on('switchChange.bootstrapSwitch', function(event) {
        var val = compo.elm.find('.bootstrap-switch').hasClass('bootstrap-switch-on');
        compo.handle_change(event, val);
    });
};
