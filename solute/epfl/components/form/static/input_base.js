epfl.FormInputBase = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid;
	var type = $(selector).closest("div").attr('epfl-type');
	var fire_change_immediately = params["fire_change_immediately"];
	
	if (type == "defaultinput" || type == "textarea" || type == "select") {
	    $(selector).change(function () {
	        if (fire_change_immediately) {
	        	epfl.dispatch_event(cid, "change", {value: $(selector).val()});
	        } else {
	        	epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: $(selector).val()}), cid);
	        }
	    });
	
	    provide_typeahead = $(selector).data("provide");
	    if (provide_typeahead == "typeahead") {
	        $(selector).typeahead({
	            source: function (query, process) {
	            	epfl.dispatch_event(cid, "typeahead", {"query":query});
	            	// todo: results have to be returned from server
	                return process(['Amsterdam', 'Washington', 'Sydney', 'Beijing', 'Cairo']);
	            }
	        });
	    }
	
	} else if (type == "checkbox") {
	    $(selector).attr('checked', $(selector).val() == 'True');
	    $(selector).change(function () {
	        var val = val = $(this).is(':checked');
	        if (fire_change_immediately) {
	        	epfl.dispatch_event(cid, "change", {value: val});
	        } else {
	        	epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	        }
	    });
	
	} else if (type == "toggle") {
	    $(selector).attr('checked', $(selector).val() == 'True');
	    $(selector).bootstrapSwitch('state');
	    $(selector).on('switchChange.bootstrapSwitch', function (event, state) {
	        var val = $(this).closest("div").parent().hasClass("bootstrap-switch-on");
	        if (fire_change_immediately) {
	        	epfl.dispatch_event(cid, "change", {value: val});
	        } else {
	        	epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	        }
	    });
	
	} else if (type == "radiobuttongroup") {
	    selector = "input[type=radio][name="+cid+"]";
	    $(selector).change(function () {
	        var val = $(this).val();
	        if (fire_change_immediately) {
	        	epfl.dispatch_event(cid, "change", {value: val});
	        } else {
	        	epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	        }
	    });
	
	} else if (type == "buttonsetgroup") {
	    selector = "input[type=radio][name="+cid+"]";
	    $(selector).change(function () {
	        var val = $(this).val();
	        var parent = $(this).parent().parent();
	        $(parent).find("label").removeClass("active");
	        $(this).parent().addClass("active");
	        if (fire_change_immediately) {
	        	epfl.dispatch_event(cid, "change", {value: val});
	        } else {
	        	epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	        }
	    });
	
	}
	if (params["submit_form_on_enter"]) {
		$(selector).bind('keyup', function(event){
			if (event.keyCode == 13) {
				epfl.dispatch_event(cid, "submit", {}); // bubbles up to form
			}
		});
	}
	if (params["input_focus"]) {
		$(selector).focus();
	}
	 
}; 
epfl.FormInputBase.inherits_from(epfl.ComponentBase);

