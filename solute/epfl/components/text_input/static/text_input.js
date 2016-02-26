epfl.TextInput = function(cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.TextInput.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.TextInput.prototype, 'form_element', {
    get: function () {
        return $("#" + this.cid + '_input');
    }
});

epfl.TextInput.prototype.handle_keypress = function(event) {
    if(this.params.max_length) {
        $("#" + this.cid + '_input' + '_count').text(this.form_element.val().length);
    }
    if(this.params.submit_form_on_enter && event.which == 13) {
        this.handle_submit_form_on_enter();
    }
};

epfl.TextInput.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    var compo = this;

    if (this.params.date) {
        this.form_element.jqDatetimepicker({
            format:'d.m.Y H:i',
            step: 15,
            closeOnTimeSelect: true,
            lang: 'de'
        });
    }

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

            var event = epfl.make_component_event(compo.cid, compo.params.type_func, {"query": query}, compo.cid + '_typeahead');
            return get_source(event);
        };
        compo.form_element.typeahead({source: type_function,
                                      items: 'all',
                                      autoSelect: false});
    }

    window.setTimeout(function () {
        if (compo.form_element.val() != compo.form_element.attr('data-initial-value')) {
            compo.handle_change.bind(compo);
        }
    }, 0);

    //this.register_change_handler();

    if (compo.params.show_count || compo.params.submit_form_on_enter) {
        compo.elm.keyup(compo.handle_keypress.bind(compo));
    }
};
