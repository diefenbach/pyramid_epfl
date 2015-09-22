epfl.Form = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Form.inherits_from(epfl.ComponentBase);


epfl.Form.prototype.after_response = function () {
    var obj = this;
	this.elm.submit(function(event) {
	    event.preventDefault();
	    obj.send_event("submit", {});
	});
};
