epfl.TableLayout = function (cid, params) {
    epfl.PaginatedListLayout.call(this, cid, params);
};

epfl.TableLayout.inherits_from(epfl.PaginatedListLayout);

Object.defineProperty(epfl.TableLayout.prototype, 'hide_column_icon', {
    get: function () {
        return this.elm.find('.hide-column-icon');
    }
});

Object.defineProperty(epfl.TableLayout.prototype, 'show_column_icon', {
    get: function () {
        return this.elm.find('.show-column-icon');
    }
});

Object.defineProperty(epfl.TableLayout.prototype, 'header_sortable', {
    get: function () {
        return this.elm.find('.header-sortable');
    }
});
Object.defineProperty(epfl.TableLayout.prototype, 'export_button', {
    get: function () {
        return $('#' + this.cid + '_export_button');
    }
});

epfl.TableLayout.prototype.handle_click = function (event) {
    epfl.PaginatedListLayout.prototype.handle_click.call(this, event);
    if (this.hide_column_icon.is(event.target)) {
        var parent_col = event.target.closest("th");
        this.send_event("hide_column", {column_index: $(parent_col).index()});
    } else if (this.show_column_icon.is(event.target)) {
        var parent_col = event.target.closest("th");
        this.send_event("show_column", {column_index: $(parent_col).index()});
    } else if (this.header_sortable.is(event.target)) {
        var parent_col = event.target.closest("th");
        this.send_event("adjust_sorting", {column_index: $(parent_col).index()});
    } else if (this.export_button.is(event.target)) {
        this.send_event("export_csv", {}, function(response){
            var type, filename;
            var result = response;
            if (jQuery.isEmptyObject(result)) {
                epfl.show_message({'msg': 'Keine Daten vorhanden.', 'typ': 'warning', 'fading': true});
                return;
            }
            type = result[0];
            if (type == 'msg') {
                epfl.show_message({'msg': result[2], 'typ': result[1], 'fading': true});
                return;
            } else {
                var data = result[1];
                if(result.length > 2) {
                    filename = result[2];
                }
                else {
                    filename = 'download.txt';
                }
                var blob = new Blob([data], {type:'text/csv'});
                saveAs(blob, filename);
            }
        });
    }
};
