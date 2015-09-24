epfl.Download = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Download.inherits_from(epfl.ComponentBase);

epfl.Download.prototype.handle_click = function(event) {
    // No super since handle_local_click is not required here
    var button_elm = $('#' + this.cid);
    if (button_elm.hasClass("disabled")) {
        return;
    }

    if (this.params["confirm_first"] && (!confirm(this.params["confirm_message"]))) {
        return;
    }
    if (this.params["disable_on_click"]) {
        button_elm.addClass("disabled");
    }

    if(this.params["event_target"]) {
        var request = epfl.make_component_event(this.params["event_target"], this.params["event_name"]);
        epfl.send(request, function(response){
            var filename;
            var result = response;
            if (jQuery.isEmptyObject(result)) {
                epfl.show_message({'msg': 'Keine Daten vorhanden.', 'typ': 'warning', 'fading': true});
                return;
            }
            var data = result[0];
            if(result.length > 1) {
                filename = result[1];
            }
            else {
                filename = 'download.txt';
            }
            var blob = new Blob([data], {type:'text/csv'});
            saveAs(blob, filename);
        });
    }
};
