epfl.ColorThief = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};
epfl.ColorThief.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.ColorThief.prototype, 'color_field', {
    get: function () {
        return this.elm.children('div.epfl-colorthief-color');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'check_icon', {
    get: function () {
        return this.elm.children('div').children('i.fa-check');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'remove_icon', {
    get: function () {
        return this.elm.children('i.epfl-colorthief-remove-icon');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'drop_zone', {
    get: function () {
        return this.elm.find('div.epfl-colorthief-dropzone');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'image', {
    get: function () {
        return this.elm.find('img');
    }
});

epfl.ColorThief.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.image.on('dragstart', function(event) { event.preventDefault(); });
};

epfl.ColorThief.prototype.handle_click = function (event) {
    epfl.FormInputBase.prototype.handle_click.call(this, event);

    var target = $(event.target);
    if (this.color_field.is(event.target)) {
        this.send_event("click_color", {"color": target.data("color")});
    } else if (this.check_icon.is(event.target)) {
        this.send_event("click_color", {"color": target.parent().data("color")});
    } else if (this.remove_icon.is(event.target)) {
        this.send_event("change", {value: null});
    }
};

epfl.ColorThief.prototype.handle_drop = function (event) {
    var obj = this;
    var imageSrc = $(event.dataTransfer.getData('text/html')).attr("src");
    if (imageSrc) {
        obj.drop_zone.hide();
        obj.image.attr("src", imageSrc);
        obj.send_event("change", {"value": null, "image_src": imageSrc});
    }else{
        var files = event.dataTransfer.files;
        var reader = new FileReader();
        reader.onload = function(){
            obj.send_event("change", {"value": null, "image_src": this.result});
        };
        reader.readAsDataURL(files[0]);
    }
    this.handle_drop_leave();
};
