epfl.NumberInput = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.NumberInput.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.NumberInput.prototype, 'input_selector', {
    'get': function() {
        return "#" + this.cid + "_input";
    }
});

epfl.NumberInput.prototype.handle_keydown = function(event) {
    var validation_type = $(this.input_selector).data('validation-type');
    var allowed_keys = [46, 8, 9, 27, 13, 110, 35, 36, 37, 38, 39, 40, 189, 109, 171, 173];
    if (validation_type === "float") {
        allowed_keys.push(190);
        allowed_keys.push(188);
        allowed_keys.push(108);
    }
    if (event.keyCode === 17) {
        this.strg = true;
    } else if (event.keyCode === 16) {
        this.shiftKey = true;
    }
    if ((event.keyCode < 48 || event.keyCode > 57 && event.keyCode < 96 || event.keyCode > 105) && allowed_keys.indexOf(event.keyCode) === -1) {
        if (this.strg && [65, 67, 86, 88].indexOf(event.keyCode) !== -1) {
        } else {
            event.preventDefault();
            return;
        }
    } else {
        if (this.shiftKey === true) {
            event.preventDefault();
            return;
        }
    }
};

epfl.NumberInput.prototype.handle_keyup = function(event) {
    if (event.keyCode === 17) {
        this.strg = false;
    } else if (event.keyCode === 16) {
        this.shiftKey = false;
    }
};

epfl.NumberInput.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    this.register_change_handler();

    this.strg = false;
    this.shiftKey = false;
    $(this.input_selector)
        .keydown(this.handle_keydown.bind(this))
        .keyup(this.handle_keyup.bind(this));

};
