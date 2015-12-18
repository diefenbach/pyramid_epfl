epfl.NumberInput = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.NumberInput.inherits_from(epfl.ComponentBase);

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

epfl.NumberInput.prototype.handle_change = function(event) {
    var enqueue_event = !this.params.fire_change_immediately;
    epfl.FormInputBase.on_change(this, $(this.input_selector).val(), this.cid, enqueue_event);
};

epfl.NumberInput.prototype.after_response = function(data) {
    this.strg = false;
    this.shiftKey = false;

    $(this.input_selector).keydown(this.handle_keydown.bind(this));
    $(this.input_selector).keyup(this.handle_keyup.bind(this));
    $(this.input_selector).change(this.handle_change.bind(this));
    $(this.input_selector).blur(this.handle_change.bind(this));
};
