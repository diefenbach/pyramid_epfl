if (typeof String.prototype.endsWith !== 'function') {
    // Check if the given string ends with the given suffix.
    // As endsWith will (should) be implemented with ES6 this might get obsolete
    String.prototype.endsWith = function(suffix){
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    }
}
if (typeof String.prototype.beginsWith !== 'function') {
    // Check if the given string ends with the given suffix.
    // As endsWith will (should) be implemented with ES6 this might get obsolete
    String.prototype.beginsWith = function(suffix){
        return this.indexOf(suffix) == 0;
    }
}

$.event.props.push('dataTransfer');

epfl.ComponentBase = function (cid, params) {
    this.cid = cid;
    this.params = params;
};

Object.defineProperty(epfl.ComponentBase.prototype, 'elm', {
    get: function () {
        return $("[epflid='" + this.cid + "']");
    }
});

epfl.ComponentBase.prototype.make_event = function (event_name, params) {
    return epfl.make_component_event(this.cid, event_name, params);
};

epfl.ComponentBase.prototype.send_event = function (event_name, params, callback) {
    epfl.send(epfl.make_component_event(this.cid, event_name, params), callback);
};

epfl.ComponentBase.prototype.send_async_event = function (event_name, params, callback) {
    epfl.send_async(epfl.make_component_event(this.cid, event_name, params), callback);
};

epfl.ComponentBase.prototype.repeat_enqueue = function (event_name, params, equiv) {
    epfl.repeat_enqueue(epfl.make_component_event(this.cid, event_name, params), equiv);
};

epfl.ComponentBase.prototype.closest_cid = function (element) {
    /* Calculates the cid of the closest epfl component containing the given element. */

    var containing_elm = $(element);
    var cid = containing_elm.attr('epflid');
    if (!cid) {
        cid = containing_elm.parent().attr('epflid');
    }
    if (!cid) {
        cid = containing_elm.parentsUntil('[epflid]').parent().attr('epflid');
    }
    return cid;
};

/* Lifecycle methods */

epfl.ComponentBase.prototype.after_response = function (data) {
    /* Called after a server response has been handled. On a full page request that is after all init steps are done,
     * during an ajax request this will be called after the response javascript has been executed or sent to the
     * callback. */
    var obj = this;
    if (this.params && this.params.extras_handle_click) {
        obj.elm.click(function (event) {
            obj.handle_click(event);
        });
    }

    if (this.params && this.params.extras_handle_drop) {
        obj.elm
            .addClass('root_drop')
            .on('dragover', function (event) {
                event.preventDefault();
                clearTimeout(obj.leave_timeout);
                // TODO: Turns out the dataTransfer is locked by CORS. Suggestions welcome.
                var moved_cid = '';
                try {
                    moved_cid = event.dataTransfer.getData('text');
                } catch (e) {}
                var current_target = obj.closest_cid(event.originalEvent.target);
                if (obj.drop_target == current_target) {
                    return;
                }
                obj.handle_drop_leave(event);
                obj.drop_target = current_target;
                obj.send_async_event('drop_accepts', {
                    cid: obj.drop_target,
                    moved_cid: moved_cid
                }, function (data) {
                    if (data === true) {
                        obj.handle_drop_accepts(event);
                    }
                });
                return true;
            })
            .on('dragleave', function (event) {
                obj.leave_timeout = setTimeout(function () {
                    obj.handle_drop_leave(event);
                }, 0);
            })
            .on('drop', function(event) {
                event.stopImmediatePropagation();
                event.preventDefault();
                obj.handle_drop(event);
            });
    }

    if (this.params && this.params.extras_handle_drag) {
        obj.elm
            .attr('draggable', true)
            .on('dragstart', function (event) {
                var dT = event.dataTransfer;
                dT.setData('text', obj.cid);
                dT.dropEffect = 'move';
                obj.handle_drag_start(event);
            });
    }

    if (this.params && this.params.extras_handle_double_click) {
        obj.elm.dblclick(function (event) {
            obj.handle_double_click(event);
        });
    }
};

epfl.ComponentBase.prototype.before_response = function (data) {
    /* Called before an ajax response is executed or sent to its callback, but after it was received from the server. */
};

epfl.ComponentBase.prototype.before_request = function () {
    /* Called before the actual ajax request is sent to the server. The queue may still be modified at this time. */
};

epfl.ComponentBase.prototype.destroy = function () {
}; // Overwrite me!

/* Predefined handle functions */

epfl.ComponentBase.prototype.handle_local_click = function (event) {
    /* Executed on click events if extras_handle_click is set to true. Local clicks are all clicks that have been
     * directly on this components html element or on any html element that has no more direct containing component. */
};

epfl.ComponentBase.prototype.is_closest = function (target) {
    /* Check if target is bound to this component's html element or to any
     * html element that has no more direct containing component. */
    var cid = this.closest_cid(target);
    return cid == this.cid;
};

epfl.ComponentBase.prototype.handle_click = function (event) {
    /* Executed on click events if extras_handle_click is set to true. */
    if (this.is_closest(event.target)) {
        this.handle_local_click(event);
    }
};

epfl.ComponentBase.prototype.handle_double_click = function (event) {
    /* Executed on double click events if extras_handle_double_click is set to true. */
};

epfl.ComponentBase.prototype.handle_drop_accepts = function (event) {
    /* Executed on EPFL drag events if extras_handle_drop is set to true. Overwrite to provide behaviour when an element
       is hovered over here. */
    if (!this.drop_target) {
        return;
    }
    var target = epfl.components[this.drop_target];
    if (!target) {
        return;
    }
    target = target.elm;
    target.addClass('active_drop');
};

epfl.ComponentBase.prototype.handle_drop_leave = function (event) {
    /* Executed on EPFL drag events if extras_handle_drop is set to true. */
    if (!this.drop_target) {
        return;
    }
    var target = epfl.components[this.drop_target];
    if (!target) {
        return;
    }
    target = target.elm;
    target.removeClass('active_drop');
    delete this.drop_target;
};

epfl.ComponentBase.prototype.handle_drop_url = function (url, event) {
    console.log('handle_drop_url', url, event);
};

epfl.ComponentBase.prototype.handle_drop_file = function (files, event) {
    console.log('handle_drop_file', files, event);
};

epfl.ComponentBase.prototype.handle_drop = function (event) {
    /* Executed on EPFL drag events if extras_handle_drag is set to true. */
    if (!event.dataTransfer) {
        return;
    }
    var text = event.dataTransfer.getData('text');
    // Text may be a cid if this is an EPFL drag event.
    if (text && epfl.components[text]) {
        epfl.components[text].send_event('drag_stop', {
            cid: this.cid,
            over_cid: this.drop_target
        });
    // If the dataTransfer contains one or more files it's treated as a file upload.
    } else if (event.dataTransfer.files.length > 0 ) {
        var files = event.dataTransfer.files;
        this.handle_drop_file(files, event);
    // If it is a url it is treated as such.
    } else if (text.beginsWith('http://') || text.beginsWith('https://') ) {
        this.handle_drop_url(text, event);
    }
    // TODO: No default behaviour is given, maybe a good place for some error handling later?

    this.handle_drop_leave();
};

epfl.ComponentBase.prototype.handle_drag_start = function (event, dd) {
    /* Executed on EPFL drag events if extras_handle_drag is set to true. Overwrite to provide behaviour when dragging
       is started. */
};
