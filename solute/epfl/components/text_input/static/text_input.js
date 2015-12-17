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


// epfl.TextInput = function (cid, params) {
//     epfl.FormInputBase.call(this, cid, params);

//     var selector = "#" + cid + "_input";
//     var compo = this;
//     var enqueue_event = !params["fire_change_immediately"];
//     var max_length = params["max_length"];
//     var show_count = params["show_count"];
//     var typeahead = params["typeahead"];
//     var type_func = params["type_func"];
//     var date = params["date"];
//     var source = params["source"];
//     var submit_form_on_enter = params["submit_form_on_enter"];

//     if(typeahead) {
//         var type_function = function(query, process){
//             var get_source = function(epfl_event){
//                 epfl.send(epfl_event, function(response){
//                     if(response && response !== "") {
//                         var i = 0, result_set = [];
//                         for (i; i < response.length; i++) {
//                             result_set.push({'id': response[i][0], 'name': response[i][1]});
//                         }
//                         process(result_set);
//                     }
//                 });
//             };

//             var event = epfl.make_component_event(cid, type_func, {"query": query}, cid + '_typeahead');
//             return get_source(event);
//         };
//         $(selector).typeahead({source: type_function,
//                                items: 'all',
//                                autoSelect: false});
//     }
//     if(date){
//         $(selector).jqDatetimepicker({
//             format:'d.m.Y H:i',
//             step: 15,
//             closeOnTimeSelect: true,
//             lang: 'de'
//         });
//     }
//     var change = function (event) {
//         epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
//     };

//     var keydown = function(event){
//         if(max_length){
//             $(selector + '_count').text($(selector).val().length);
//         }
//         if(submit_form_on_enter && event.which == 13){
//             epfl.FormInputBase.event_submit_form_on_enter(cid);
//         }
//     };

//     var elm = $(selector);

//     window.setTimeout(function () {
//         if (elm.val() != elm.attr('data-initial-value')) {
//             change();
//         }
//     }, 0);

//     elm.blur(change).change(change);
//     if(show_count || submit_form_on_enter){
//         elm.keydown(keydown);
//     }
// };

// epfl.TextInput.inherits_from(epfl.FormInputBase);
