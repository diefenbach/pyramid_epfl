epfl.Carousel = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Carousel.inherits_from(epfl.ComponentBase);

epfl.Carousel.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    this.elm.carousel();

    var object = this.elm;
    this.elm.on('slid.bs.carousel', function() {
        var total_items = object.find('div.item').length;
        var current_index = object.find('div.active').index() + 1;
        object.find('div.carousel-numbers').html(current_index + ' / ' + total_items);
    });
};
