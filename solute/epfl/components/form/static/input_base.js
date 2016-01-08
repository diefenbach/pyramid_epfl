epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.FormInputBase.inherits_from(epfl.ComponentBase);

epfl.FormInputBase.prototype.add_custom_style = function(style) {
    this.elm.find('input, select').attr('style', style);
};

epfl.FormInputBase.prototype.after_response = function(data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);

    if (this.params.input_style !== "None") {
        this.add_custom_style(this.params.input_style);
    }
};

epfl.FormInputBase.prototype.handle_submit_form_on_enter = function () {
    // delegate the submit event to the form
    var parent_form = this.elm.closest('.epfl-form');
    parent_form.submit();
};

epfl.FormInputBase.prototype.send_change = function(event, value) {
    /* takes the value and send the epfl event */
    if (value === undefined) {
        value = $(event.target).val();
    }

    var enqueue_event = !this.params.fire_change_immediately;
    if (enqueue_event === undefined) {
        enqueue_event = true;
    }

    var parent_form = this.elm.closest('.epfl-form');
    if (parent_form.length == 1) {
    	var is_dirty = parent_form.data('dirty');
	if (is_dirty == '0') {
	    parent_form.data('dirty', '1');
	    // first change to the form. always send event immediately so that
	    // the serve can handle is_dirty change
	    enqueue_event = false;
            this.repeat_enqueue('set_dirty', {}, this.cid + "_set_dirty");
	}
    }
    if (enqueue_event) {
        this.repeat_enqueue('change', {value: value}, this.cid + "_change");
    } else {
        this.send_event('change', {value: value});
    }
};

epfl.FormInputBase.prototype.handle_change = function(event, value) {
    /* takes the value and send the epfl event if the value really changed */
    if (value === undefined) {
        value = $(event.target).val();
    }

    if (value !== this.lastValue) {
        this.lastValue = value;
        this.send_change(event, value);
    }
};

epfl.FormInputBase.prototype.handle_keydown = function(event) {
    if (event.which == 13) {
        this.handle_submit_form_on_enter();
    }
};

epfl.FormInputBase.prototype.register_change_handler = function() {
    /* if the compo has a form_element set, register it with blur() and change() events
       to trigger handle_change */
    if (this.form_element && this.form_element.length) {
        this.form_element.blur(this.handle_change.bind(this)).change(this.handle_change.bind(this));
    } else {
        console.log('Called FromInputBase.register_change_handler without set form_element',
                    this.form_element);
    }
};

epfl.FormInputBase.prototype.register_submit_form_on_enter_handler = function() {
   /* if the compo has a form_element set, register it with blur() and change() events
       to trigger handle_change */
    if (this.form_element && this.form_element.length) {
        if (this.params.submit_form_on_enter) {
            this.form_element.keydown(this.handle_keydown.bind(this));
        }
    } else {
        console.log('Called FromInputBase.register_submit_form_on_enter_handler without set form_element',
                    this.form_element);
    }
};
