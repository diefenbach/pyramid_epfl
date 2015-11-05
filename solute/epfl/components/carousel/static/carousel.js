epfl.Carousel = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Carousel.inherits_from(epfl.ComponentBase);

epfl.Carousel.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    $("#" + this.cid).carousel();
};
