epfl.TypeAhead = function(cid, params) {
    epfl.LinkListLayout.call(this, cid, params);
};
epfl.TypeAhead.inherits_from(epfl.LinkListLayout);

epfl.TypeAhead.prototype.handle_local_click = function (event) {
    epfl.LinkListLayout.prototype.handle_local_click.call(this, event);
    var btn = this.dropdown_toggle;

    if (btn.is(event.target)) {
        this.update_visibility(true);
    }
};

Object.defineProperty(epfl.TypeAhead.prototype, 'list', {
    get: function () {
        return this.elm.find('.epfl-typeahead-list');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'search_input', {
    get: function () {
        return this.elm.find('#' + this.cid + '_search');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'dropdown_toggle', {
    get: function () {
        return this.elm.children('div').children('div.btn.fa.fa-caret-down');
    }
});

epfl.TypeAhead.prototype.update_visibility = function (toggle) {
    var available_entries = this.elm.find('[data-parent-epflid=' + this.cid + ']');
    if (available_entries.length == 0 ||
        (!this.search_input.is(':focus') && this.elm.find(':hover').length == 0)) {
        this.list.hide();
    } else if (toggle) {
        this.list.toggle();
    } else {
        this.list.show();
    }
};

epfl.TypeAhead.prototype.after_response = function (data) {
    epfl.LinkListLayout.prototype.after_response.call(this, data);

    var obj = this;
    obj.list.hide().css({
        position: 'absolute',
        padding: 0,
        zIndex: 10,
        width: '100%',
        maxHeight: 200,
        overflow: 'auto'
    });

    obj.search_input
        .focus(function () {
            update_visibility();
        })
        .focusout(function () {
            update_visibility();
        });
    if (obj.params.open_on_hover) {
        obj.elm
            .mouseenter(function () {
                update_visibility();
            })
            .mouseout(function () {
                update_visibility();
            });
    }

    obj.elm.keydown(function (event) {
        var available_entries = obj.elm.find('[data-parent-epflid=' + obj.cid + ']');
        var active_entry = obj.elm.find('[data-parent-epflid=' + obj.cid + '].active');
        var position = -1;

        available_entries.each(function (i, elm) {
            if (active_entry.is(elm)) {
                position = i;
            }
        });
        switch (event.keyCode) {
            case 13: // enter
                var active_compo = epfl.components[active_entry.attr('epflid')];
                active_compo.handle_click({target: active_entry, originalEvent: {preventDefault: function () {}}});
                break;
            case 38: // arrow up
                position -= 1;
                break;
            case 40: // arrow down
                position += 1;
                break;
            default:
                return;
        }
        if (position == -2) {position = -1;} // Only happens on key up with no selected entry.

        available_entries.removeClass('active');

        position %= available_entries.length;
        available_entries.eq(position).addClass('active');
        setTimeout(function () {
            var current_entry = available_entries.eq(position);
            if(current_entry.length !== 0) {
                obj.list.scrollTop(
                    current_entry.offset().top - obj.list.offset().top + obj.list.scrollTop() - current_entry.outerHeight()
                );
            }
        }, 0);
    });


    function update_visibility() {
        setTimeout(function () {
            obj.update_visibility();
        }, 0);
    }
    update_visibility();

};
