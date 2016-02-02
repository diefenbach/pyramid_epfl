(function () {
    function get_epflid(containing_elm) {
        return $(containing_elm).closest('[epflid]').attr('epflid');
    }

    function line_marker() {
        $('.drop-line-marker').remove();
        var arrow_l = $('<i class="pull-left fa fa-arrow-up" />');
        var arrow_r = $('<i class="pull-right fa fa-arrow-up" />');
        return $('<div></div>')
            .append(arrow_l)
            .append(arrow_r)
            .css('width', '100%')
            .css('height', '10px')
            .css('margin-top', '-10px')
            .css('overflow', 'show')
            .css('border-top', '1px solid black')
            .addClass('drop-line-marker');
    }

    var drag_stop = function(cid) {
        return function (elm, type, data) {
            data.over_cid = $('[epflid=' + data.over_cid + ']')
                .closest('[epflid][data-parent-epflid=' + cid + ']').attr('epflid');
            return true;
        };
    };

    var remove_line_marker = function() {
        $('.drop-line-marker').remove();
    };

    var drop_accepts = function(cid) {
        return function (elm, type, data) {
            var target_elm = $(data.originalEvent.target).closest('[epflid][data-parent-epflid=' + cid + ']');
            var target_cid = target_elm.attr('epflid');

            delete data.originalEvent;
            delete data.elm;

            if (target_cid) {
                line_marker()
                    .insertBefore($('[epflid=' + target_cid + ']'));
            } else {
                line_marker()
                    .appendTo($('[epflid=' + cid + ']'));
            }

            elm.mouseout(function (e) {
                var elem = $(e.target);
                if (elem.attr('epflid') != cid) {
                    return;
                }
                $(this).unbind('mouseout');
                remove_line_marker();
            });
        };
    };

    epfl.set_drop_zone = function (cid) {
        var elm = $('[epflid=' + cid + ']');

        epfl.set_component_info(cid, 'before_send_event', 'drop_accepts', drop_accepts(cid));
        epfl.set_component_info(cid, 'before_send_event', 'drag_stop', drag_stop(cid));
        epfl.set_component_info(cid, 'callback_send_event', 'drag_stop', remove_line_marker);
    };
})();