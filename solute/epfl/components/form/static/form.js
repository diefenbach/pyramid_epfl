epfl.Form = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Form.inherits_from(epfl.ComponentBase);


epfl.Form.prototype.after_response = function () {
    var compo = this;
    this.elm.submit(function(event) {
        compo.trigger('Submit', {});
	event.preventDefault();
//	compo.send_event(compo.params.event_name, {});
    });
};
