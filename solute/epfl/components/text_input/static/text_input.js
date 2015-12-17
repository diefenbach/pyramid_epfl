epfl.TextInput = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.TextInput.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.TextInput.prototype, 'input_selector', {
    get: function () {
        return "#" + this.cid + '_input';
    }
});

epfl.TextInput.prototype.handle_keypress = function(event) {
    if(this.params.max_length) {
        $(this.input_selector + '_count').text($(this.input_selector).val().length);
    }
    if(this.params.submit_form_on_enter && event.which == 13) {
        console.log(1);
        epfl.FormInputBase.event_submit_form_on_enter(this.cid);
    }
};

epfl.TextInput.prototype.handle_change = function(event) {
    var enqueue_event = !this.params["fire_change_immediately"];
    epfl.FormInputBase.on_change(this, $(this.input_selector).val(), this.cid, enqueue_event);
};

epfl.TextInput.prototype.after_response = function(data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    var obj = this;
    var input_elm = $(obj.input_selector);

    if (this.params.date) {
        $(this.input_selector).jqDatetimepicker({
            format:'d.m.Y H:i',
            step: 15,
            closeOnTimeSelect: true,
            lang: 'de'
        });
    }


    // form submit always?

    if (this.params.typeahead) {
        var type_function = function(query, process){
            var get_source = function(epfl_event){
                epfl.send(epfl_event, function(response){
                    if(response && response !== "") {
                        var i = 0, result_set = [];
                        for (i; i < response.length; i++) {
                            result_set.push({'id': response[i][0], 'name': response[i][1]});
                        }
                        process(result_set);
                    }
                });
            };

            var event = epfl.make_component_event(obj.cid, obj.params.type_func, {"query": query}, obj.cid + '_typeahead');
            return get_source(event);
        };
        $(obj.input_selector).typeahead({source: type_function,
                               items: 'all',
                               autoSelect: false});
    }

    window.setTimeout(function () {
        if (input_elm.val() != input_elm.attr('data-initial-value')) {
            obj.handle_change.bind(obj);
        }
    }, 0);

    obj.elm.blur(obj.handle_change.bind(obj)).change(obj.handle_change.bind(obj));

    if (obj.params.show_count || obj.params.submit_form_on_enter) {
        obj.elm.keyup(obj.handle_keypress.bind(obj));
    }
};
