
if (typeof Object.create !== 'function') {
    Object.create = function (o) {
        function F() {};
        F.prototype = o;
        return new F();
    };
} // for older browsers
Function.prototype.inherits_from = function(super_constructor) {
    this.prototype = Object.create(super_constructor.prototype);
    this.prototype.constructor = super_constructor;
}; // inheritance

var epfl = new Object();

if (window.epfl_flush_active === undefined) {
    window.epfl_flush_active = false;
}

if (window.epfl_flush_again === undefined) {
    window.epfl_flush_again = false;
}



epfl_module = function() {

    epfl.queue = [];
    epfl.event_id = 0;
    epfl.components = {};
    epfl.component_data = {};
    epfl.show_please_wait_counter = 0;

    epfl.init_page = function(opts) {
        $(".epfl_hover_image").bind_hover_border_events();
        $("body").append("<div id='epfl_please_wait'><i class='fa fa-spinner fa-spin fa-5x text-primary'></i></div>");

        $("#loader").remove(); // remove the std-mcp2 ajax-loader image

/*        var scroll_pos = $(".epfl_scroll_pos").val(); // Restoring Scroll-Pos
        if (scroll_pos) {
            var tmp = scroll_pos.split("x");
            $(document).scrollLeft(parseInt(tmp[0]));
            $(document).scrollTop(parseInt(tmp[1]));
        };


        $(window).scroll(function() { // Capturing Scroll-Pos
            var scroll_pos = $(document).scrollLeft() + "x" + $(document).scrollTop();
            $(".epfl_scroll_pos").val(scroll_pos)
        });
*/

        epfl.new_tid(opts["tid"], true);
        epfl.ptid = opts["ptid"];
        epfl.log_time = opts["log_time"];
        $(document).attr("data:tid", epfl.tid);
        epfl.init_struct();
        epfl.after_response();
    };

    epfl.dispatch_event = function (elm, type, data) {
        alert('This software is using a deprecated method and will not work correctly with this EPFL Version!')
    };

    epfl.set_component_info = function (cid, key, value, extra_value) {
        if (!epfl.component_data[cid]) {
            epfl.component_data[cid] = {};
        }
        if (!extra_value) {
            return epfl.component_data[cid][key] = value;
        }
        if (!epfl.component_data[cid][key]) {
            epfl.component_data[cid][key] = {};
        }
        epfl.component_data[cid][key][value] = extra_value;
    };

    epfl.init_struct = function () {
        if (epfl.init_struct_timeout) {
            clearTimeout(epfl.init_struct_timeout);
        }
        epfl.init_struct_timeout = setTimeout(function () {
            $('[epflid]').each(function (i, elm) {
                elm = $(elm);
                elm.attr('data-parent-epflid', elm.parent().closest('[epflid]').attr('epflid'));
            });
        }, 0);
    };

    epfl.init_component = function(cid, class_name, params) {
        var constructor = epfl[class_name];
        if (!constructor) {
            console.log("JS-ERROR: The component '" + class_name + "' does not exist!");
            return;
        }
        var compo_obj = new constructor(cid, params);
        epfl.components[cid] = compo_obj;
    };

    epfl.replace_component = function(cid, parts) {
        for (var part_name in parts) {
            if (part_name == "js") continue;
            if (part_name == "prefetch") continue;
            var part_html = parts[part_name];
            var epflid = cid;
            if (part_name != "main") {
                epflid = cid + "$" + part_name;
            }
            var el = $("[epflid='" + epflid + "']");
            if (el.length == 0) {
                console.log("Element not found!", cid, parts);
                return;
            }
            var parts_jq = $(part_html);
            if (parts["prefetch"]) {
                $.ajax(parts["prefetch"], {async: false});
            }
            el.replaceWith(parts_jq);
            epfl.init_struct();
        }
        eval(parts["js"]);
    };

    epfl.hide_component = function(cid) {
          $("[epflid='" + cid + "']").replaceWith("<div epflid='" + cid + "'></div>");
    };

    epfl.switch_component = function(cid) {
        $('[epflid=' + cid + ']').remove();
    };

    epfl.destroy_component = function(cid) {
        var compo = epfl.components[cid];
        if (compo) {
            compo.destroy();
            delete epfl.components[cid];
        }
        $('[epflid=' + cid + ']').remove();
    };

    epfl.unload_page = function() {
        epfl.flush(null, true);
    };

    epfl.flush_queue = [];
    epfl.flush_queue_active = false;

    epfl.flush = function (callback_func, sync) {

        if (epfl.queue.length == 0) {
            // queue empty
            if (callback_func) {
                callback_func(null);
            }
            return;
        }

        epfl.flush_queue.push([callback_func, sync, epfl.queue]);
        epfl.queue = [];
        epfl.flush_queued();
    };

    epfl.flush_queued = function () {
        if (epfl.flush_queue_active || epfl.flush_queue.length == 0) {
            return;
        }
        epfl.before_request();
        epfl.flush_queue_active = true;
        var flush = epfl.flush_queue.shift();
        epfl.flush_unqueued(flush[0], flush[1], flush[2]);
    };

    epfl.flush_unqueued = function (callback_func, sync, queue) {
        if (window.epfl_flush_active) {
            window.epfl_flush_again = true;
            return;
        }

        if (epfl.show_please_wait_counter > 0) {
            sync = true;
        }

        epfl.show_please_wait(true);

        return epfl.post_event(queue, sync, callback_func);
    };

    epfl.post_event = function (queue, sync, callback_func, unqueued) {

        return $.ajax({
            url: location.href,
            global: false,
            async: !sync,
            type: "POST",
            cache: false,
            data: JSON.stringify({"tid": epfl.tid, "q": queue, unqueued: unqueued}),
            contentType: "application/json",
            dataType: "text",
            success: function (data) {
                try {
                    data = $.parseJSON(data);
                    epfl.before_response(data);
                } catch(e) {
                    if (e.name != 'SyntaxError') {
                        throw e;
                    }
                    try {
                        epfl.before_response();
                        var start;
                        try {
                            start = window.performance.now();
                        } catch(e) {}
                        $.globalEval(data);
                        try {
                            if (epfl.log_time && start && !unqueued) {
                                var time_used = window.performance.now() - start;
                                epfl.send_async(epfl.make_page_event("log_time", {time_used: time_used}));
                            }
                        } catch (e) {}
                    } catch(e) {
                        epfl.show_message({"msg": "Error (" + e.name + ") when running Server response: " + e.message, "typ": "error", "fading": true});
                    }
                }
                if (callback_func) {
                    callback_func(data);
                }
                epfl.after_response();
                if (unqueued) {
                    return;
                }
                epfl.hide_please_wait(true);
            },
            error: function (httpRequest, message, errorThrown) {
                epfl.show_message({"msg": "Server Error: " + errorThrown, "typ": "error", "fading": true});
                console.log(httpRequest);
                if (unqueued) {
                    return;
                }
                epfl.hide_please_wait(true);
            },
            complete: function (jqXHR, status) {
                if (unqueued) {
                    return;
                }
                epfl.flush_queue_active = false;
                epfl.flush_queued();
            }
        });
    };

    epfl.send = function(epflevent, callback_func) {
        epfl.enqueue(epflevent);
        epfl.flush(callback_func);
    };

    epfl.send_async = function(epflevent, callback_func) {
        epfl.post_event([epflevent], false, callback_func, true);
    };

    epfl.enqueue = function(epflevent) {
        epfl.queue.push(epflevent);
    };

    epfl.repeat_enqueue = function(epflevent, equiv) {
        for (var i = 0; i < epfl.queue.length; i++) {
            if (epfl.queue[i]["eq"] == equiv) {
                epfl.queue.splice(i, 1);
                break;
            };
        };
        epflevent["eq"] = equiv;
        epfl.enqueue(epflevent);
    };

    epfl.dequeue = function(equiv) {
        var new_queue = [];
        for (var i = 0; i < epfl.queue.length; i++) {
            if (epfl.queue[i]["eq"] != equiv) {
                new_queue.push(epfl.queue[i]);
            };
        };
        epfl.queue = new_queue;
    };


    epfl.make_component_event = function(component_id, event_name, params, lazy_mode) {

        if (!params) params = {};
        if (!lazy_mode) lazy_mode = false;

        return {"id": epfl.make_event_id(),
                "t": "ce",
                "lazy_mode": lazy_mode,
                "cid": component_id,
                "e": event_name,
                "p": params};
    };

    epfl.make_page_event = function(event_name, params) {

        if (!params) params = {};

        return {"id": epfl.make_event_id(),
                "t": "pe",
                "e": event_name,
                "p": params};
    };

    epfl.make_event_id = function() {
        epfl.event_id += 1;
        return epfl.event_id;
    };

    epfl.json_request = function(event, callback_func) {
        epfl.flush(function() {
            var ajax_target_url = location.href;
            $.ajax({url: ajax_target_url,
                    global: false,
                    type: "POST",
                    cache: false,
                    data: JSON.stringify({"tid": epfl.tid, "q": [event]}),
                    contentType: "application/json",
                    dataType: "json",
                    success: function(data) { callback_func(data) },
                    error: function(httpRequest, message, errorThrown) {
                        epfl.show_message({"msg": "txt_system_error: " + errorThrown, "typ": "error", "fading": true});
                    }
                   });
        });
    };


    epfl.show_please_wait = function(is_ajax) { // Should be called as onsubmit
        if (is_ajax) {
            epfl.show_please_wait_counter += 1;
        } else {
            epfl.show_please_wait_counter = 1;
        }
        if (epfl.show_please_wait_counter == 1) {
            $('#epfl_please_wait').fadeIn();
        } else {
            $('#epfl_please_wait').stop(true);
            $('#epfl_please_wait').show();
        }
        $('#epfl_please_wait').center();
    };

    epfl.hide_please_wait = function(is_ajax) { // Should be called as onsubmit
        if (is_ajax) {
            epfl.show_please_wait_counter -= 1;
        } else {
            epfl.show_please_wait_counter = 0;
        }
        if (epfl.show_please_wait_counter == 0) {
            $('#epfl_please_wait').stop(true);
            $('#epfl_please_wait').fadeOut();
        };
    };

    epfl.show_message = function(params) {
        var msg = params['msg'];
        var typ = params['typ'];
        var fading = params['fading'];
        fading = fading || false;
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": false,
            "progressBar": false,
            "positionClass": "toast-bottom-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": (fading ? "5000" : "0"),
            "extendedTimeOut": (fading ? "1000" : "0"),
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut",
            "tapToDismiss": fading || false
        };
        if (typ == "info") {
            toastr.info(msg);
        } else if (typ == "ok") {
            toastr.success(msg);
        } else if (typ == "success") {
            toastr.success(msg);
        } else if (typ == "error") {
            toastr.error(msg);
        } else if (typ == "warning") {
            toastr.warning(msg);
        } else {
            alert(msg);
        }
    };

    epfl.reload_page = function() {
        var frm = $('<form id="__epfl_submit_form__" method="POST" action="#"></form>');
        frm.append('<input type="hidden" name="tid" value="' + epfl.tid + '">');
        $(document.body).append(frm);
        $("#__epfl_submit_form__").submit();
        $("#__epfl_submit_form__").remove();
    };

    epfl.go_next = function(target_url) {
        var frm = $('<form id="__epfl_submit_form__" method="POST" action="' + encodeURI(target_url) + '"></form>');
        frm.append('<input type="hidden" name="tid" value="' + epfl.tid + '"');
        $(document.body).append(frm);
        $("#__epfl_submit_form__").submit();
        $("#__epfl_submit_form__").remove();
    };

    epfl.jump = function(target_url) {
        var frm = $('<form id="__epfl_submit_form__" method="POST" action="' + encodeURI(target_url) + '"></form>');
        $(document.body).append(frm);
        $("#__epfl_submit_form__").submit();
        $("#__epfl_submit_form__").remove();
    };

    epfl.jump_extern = function(target_url, target) {
        var win = window.open(target_url, target);
        win.focus();
    };

    epfl.exec_in_page = function(tid, js_src, search_downwards) {
        if (epfl.tid == tid) {
            eval(js_src);
        } else {
            window.top.epfl.exec_in_page(tid, js_src, true);
        }
    };

    epfl.handle_dynamic_extra_content= function(content) {
        content.forEach(function (data) {
            $(document.body).append(data)
        });
    };

    epfl.new_tid = function (tid, initial) {
        epfl.tid = tid;

        // Get existing GET parameters
        var number_sign_pos = window.location.search.indexOf('#');
        var prmstr;
        if (number_sign_pos > 0) {
            prmstr = window.location.search.substr(1, number_sign_pos);
        } else {
            prmstr = window.location.search.substr(1);
        }
        var params = {};
        if (prmstr != null && prmstr != "") {
            var prmarr = prmstr.split("&");
            for ( var i = 0; i < prmarr.length; i++) {
                var tmparr = prmarr[i].split("=");
                if (tmparr[0] != "tid") {
                    params[tmparr[0]] = tmparr[1];
                }
            }
        }
        var target_url = window.location.pathname + "?tid=" + tid;
        if (Object.keys(params).length > 0) {
            for (var p in params) {
                if (params.hasOwnProperty(p)) {
                    target_url += "&" + p + "=" + params[p];
                }
            }
        }
        if (initial) {
            History.replaceState({tid: tid}, window.document.title, target_url);
        } else {
            History.pushState({tid: tid}, window.document.title, target_url);
        }
    };

    History.Adapter.bind(window,'statechange',function(){
        var state = History.getState();
        if (epfl.tid == state.data.tid) {
            return;
        }
        epfl.tid = state.data.tid;
        epfl.send(epfl.make_page_event('redraw_all'));
    });

    /* Lifecycle methods */
    epfl.before_request = function () {
        for (var cid in epfl.components) {
            epfl.components[cid].before_request();
        }
    };

    epfl.before_response = function (data) {
        for (var cid in epfl.components) {
            epfl.components[cid].before_response(data);
        }
    };

    epfl.after_response = function () {
        for (var cid in epfl.components) {
            var compo = epfl.components[cid];
            if (compo._elm && compo._elm.get(0) == compo.elm.get(0)) {
                continue;
            }
            compo.after_response();
            compo._elm = compo.elm;
        }
    };

};

epfl_module();

$(window).bind("beforeunload", epfl.unload_page);

(function($) {
    jQuery.fn.extend({
        highlight_hover_border: function () {
            this.removeClass("epfl_hover_image");
            this.addClass("epfl_hover_image_selected");
            this.unbind_hover_border_events();
            this.css("border-color", "blue");
        },
        unhighlight_hover_border: function () {
            this.addClass("epfl_hover_image");
            this.removeClass("epfl_hover_image_selected");
            this.bind_hover_border_events();
            this.css("border-color", "transparent");
        },
        unbind_hover_border_events: function () {
            this.unbind("mouseenter mouseleave");
        },
        bind_hover_border_events: function () {
            this.hover(
                function () {
                    $(this).css("border-color", "#8080ff");
                },
                function () {
                    $(this).css("border-color", "transparent");
                });
        },
        center: function (parent) {
            if (parent) {
                parent = this.parent();
            } else {
                parent = window;
            }
            this.css({
                "position": "absolute",
                "top": ((($(parent).height() - this.outerHeight()) / 2) + $(parent).scrollTop() + "px"),
                "left": ((($(parent).width() - this.outerWidth()) / 2) + $(parent).scrollLeft() + "px")
            });
        }
    });
})(jQuery);
