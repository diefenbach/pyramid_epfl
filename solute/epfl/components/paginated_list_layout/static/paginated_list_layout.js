epfl.PaginatedListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.PaginatedListLayout.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.PaginatedListLayout.prototype, 'orderby', {
    get: function () {
        return this.elm.find("#" + this.cid + '_orderby');
    }
});

Object.defineProperty(epfl.PaginatedListLayout.prototype, 'ordertype', {
    get: function () {
        return this.elm.find("#" + this.cid + '_ordertype');
    }
});

Object.defineProperty(epfl.PaginatedListLayout.prototype, 'search', {
    get: function () {
        return this.elm.find("#" + this.cid + '_search');
    }
});

Object.defineProperty(epfl.PaginatedListLayout.prototype, 'pagination', {
    get: function () {
        return this.elm.find("#" + this.cid + '_pagination');
    }
});

Object.defineProperty(epfl.PaginatedListLayout.prototype, 'list', {
    get: function () {
        return this.elm.find('.epfl-list');
    }
});


epfl.PaginatedListLayout.prototype.send_row_update = function (data, callback) {
    var obj = this;
    var _data = {
        row_data: obj.params.row_data,
        row_limit: obj.params.row_limit,
        row_offset: obj.params.row_offset
    };
    for (var key in data) {
        _data[key] = data[key];
    }
    obj.send_event('set_row', _data, callback);
};

epfl.PaginatedListLayout.prototype.submit = function () {
    var obj = this;
    try {
        if (obj.search.val() == obj.params.row_data['search']) {
            return;
        }
    } catch (e) {
    }

    if (obj.search.prev().prop("tagName") != "SPAN") {
        obj.search
            .before($("<span></span>")
                .addClass("fa fa-spinner fa-spin")
                .css("margin-right", "25px")
            );
    }
    var row_data = obj.params.row_data;
    if (!row_data) {
        row_data = {};
    }

    if (obj.orderby.length && obj.ordertype.length) {
        row_data.orderby = obj.orderby.find("option:selected").val();
        row_data.ordertype = obj.ordertype.find("option:selected").val();
    }

    row_data.search = obj.search.val();
    obj.send_row_update({row_data: row_data}, function () {
        if (obj.search && obj.search.prev().prop("tagName") == "SPAN") {
            obj.search.prev().remove();
            obj.search.parent().removeClass("has-feedback");
        }
    });
};

epfl.PaginatedListLayout.prototype.after_response = function () {
    epfl.ComponentBase.prototype.after_response.call(this);
    var obj = this;

    if (obj.params.show_search) {
        var search_timeout;
        var preventSubmit = function (event) {
            if (event.key == 'Enter') {
                event.preventDefault();
                return false;
            }
        };
        obj.search.keyup(function (event) {
            if (search_timeout) {
                clearTimeout(search_timeout);
            }
            if (event.key == 'Enter') {
                obj.submit();
                return preventSubmit(event);
            } else {
                search_timeout = setTimeout(obj.submit.bind(obj), obj.params.search_timeout || 500);
            }
        });

        if (obj.params.search_focus) {
            // Bugfix: focus fails if triggered without this timeout.
            setTimeout(function () {
                obj.search.focus();
                obj.search[0].setSelectionRange(obj.search.val().length, obj.search.val().length);
            });
        }
    }

    if (obj.params.show_pagination) {
        obj.pagination.click(function (event) {
            if ($(event.target.parentNode).hasClass('disabled')) {
                return;
            }
            var target_string = event.target.textContent;
            var selected_offset;
            switch (target_string) {
                case '«':
                    selected_offset = 0;
                    break;
                case '»':
                    selected_offset = Math.floor(obj.params.row_count / obj.params.row_limit);
                    break;
                case '<':
                    selected_offset = Math.floor(obj.params.row_offset / obj.params.row_limit) - 1;
                    break;
                case '>':
                    selected_offset = Math.floor(obj.params.row_offset / obj.params.row_limit) + 1;
                    break;
                default:
                    selected_offset = parseInt(target_string) - 1;
            }
            if (selected_offset * obj.params.row_limit != obj.params.row_offset) {
                obj.send_row_update({row_offset: selected_offset * obj.params.row_limit})
            }
        });
    }
    else if (obj.params.infinite_scrolling) {
        function relativeOffset(elm) {
            elm = $(elm);
            var pos = elm.position().top;
            if (!elm.offsetParent().is(elm.parent())) {
                pos = pos - elm.parent().position().top;
            }
            return pos;
        }

        var firstChild = obj.list.children().first();
        var lastChild = obj.list.children().last();
        firstChild.css('margin-top', firstChild.outerHeight() * obj.params.row_offset);
        lastChild.css(
            'margin-bottom',
            lastChild.outerHeight() * (obj.params.row_count - obj.params.row_offset - obj.params.row_limit)
        );
        obj.list.scrollTop(firstChild.outerHeight() * obj.params.row_offset);

        if (epfl.scroll_memory && epfl.scroll_memory[obj.cid]) {
            obj.list.scrollTop(epfl.scroll_memory[obj.cid]);
        } else {
            if (!epfl.scroll_memory) {
                epfl.scroll_memory = {};
            }
            epfl.scroll_memory[obj.cid] = undefined;
        }

        var trigger_range = obj.params.row_limit / 5;
        var shift = obj.params.row_limit / 2;

        window.setTimeout(function () {

            var listener = obj.list.scroll($.debounce(100, function (event) {
                var visible_children = [];
                var height = obj.list.outerHeight();
                var total_children = 0;

                obj.list.children().each(function (i, c) {
                    total_children++;
                    c = $(c);
                    var pos = relativeOffset(c);

                    if (pos + c.height() < 0 || pos > height) {
                        return;
                    }
                    visible_children.push(c)
                });

                epfl.scroll_memory[obj.cid] = obj.list.scrollTop();

                if (visible_children.length <= 1) {
                    firstChild = obj.list.children().first();
                    var scroll_position = parseInt(epfl.scroll_memory[obj.cid] / firstChild.outerHeight());
                    obj.list.unbind('scroll', listener);
                    obj.send_row_update({row_offset: Math.max(0, scroll_position - shift)});
                    return;
                }

                var first_visible_child = visible_children.shift();
                var first_visible_child_index = first_visible_child.index();

                var last_visible_child_index = visible_children.pop().index();

                // First visible child has index < 5 and row_offset is greater than 0.
                if (first_visible_child_index < trigger_range && obj.params.row_offset > 0) {
                    obj.list.unbind('scroll', listener);
                    obj.send_row_update({row_offset: Math.max(0, obj.params.row_offset - shift)});
                }

                // Last visible child has index > total_children - 5 and row_offset is lesser than row_count.
                else if (last_visible_child_index > total_children - trigger_range
                    && obj.params.row_offset + obj.params.row_limit < obj.params.row_count) {
                    obj.list.unbind('scroll', listener);
                    obj.send_row_update({row_offset: Math.max(0, obj.params.row_offset + shift)});
                }
            }));
        }, 0);
    }
};
