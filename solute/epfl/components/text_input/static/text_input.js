epfl.TextInput = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var max_length = params["max_length"];
    var show_count = params["show_count"];
    var typeahead = params["typeahead"];
    var type_func = params["type_func"];
    var date = params["date"];
    var source = params["source"];
    var submit_form_on_enter = params["submit_form_on_enter"];

    if(typeahead) {
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

            var event = epfl.make_component_event(cid, type_func, {"query": query}, cid + '_typeahead');
            return get_source(event);
        };
        $(selector).typeahead({source: type_function,
                               items: 'all',
                               autoSelect: false});
    }
    if(date){
        $(selector).jqDatetimepicker({
            format:'d.m.Y H:i',
            closeOnTimeSelect: true,
            lang: 'de'
        });
    }
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
    };

    var keydown = function(event){
        if(max_length){
            $(selector + '_count').text($(selector).val().length);
        }
        if(submit_form_on_enter && event.which == 13){
            epfl.FormInputBase.event_submit_form_on_enter(cid);
        }
    };

    window.setTimeout(function () {
        if (compo.elm.val() != compo.elm.attr('data-initial-value')) {
            change();
        }
    }, 0);

    compo.elm.blur(change).change(change);
    if(show_count || submit_form_on_enter){
        compo.elm.keydown(keydown);
    }
};

epfl.TextInput.inherits_from(epfl.FormInputBase);
