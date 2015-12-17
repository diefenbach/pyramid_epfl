epfl.Toggle = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Toggle.inherits_from(epfl.ComponentBase);

epfl.Toggle.prototype.after_response = function(data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);

    var obj = this;
    var enqueue_event = !this.params.fire_change_immediately;
    var selector = "#" + this.cid + "_input";

    $(selector).attr('checked', $(selector).val() == 'True');
    $(selector).bootstrapSwitch('state');

    $(selector).on('switchChange.bootstrapSwitch', function (event, state) {
        var val = obj.elm.find('.bootstrap-switch').hasClass('bootstrap-switch-on');
        epfl.FormInputBase.on_change(obj, val, obj.cid, enqueue_event);
    });
};
