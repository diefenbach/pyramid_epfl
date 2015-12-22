epfl.ButtonRadio = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.ButtonRadio.inherits_from(epfl.ComponentBase);

epfl.ButtonRadio.prototype.after_response = function(data) {
    var selector = "input[type=radio][name=" + this.cid + "]";
    var obj = this;
    var enqueue_event = !this.params.fire_change_immediately;

    $(selector).change(function() {
        epfl.FormInputBase.on_change(obj, $(this).val(), obj.cid, enqueue_event);
    });
};
