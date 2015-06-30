epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Upload.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.TypeAhead.prototype, 'input_selector', {
    get: function () {
        return this.elm.find('#' + this.cid + '_input');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'img_container', {
    get: function () {
        return this.elm.find('#' + this.cid + '_img');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'drop_zone', {
    get: function () {
        return this.elm.find('div.epfl-dropzone');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'image', {
    get: function () {
        return this.elm.find('img.epfl-upload-image');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'add_icon', {
    get: function () {
        return this.elm.find('p.epfl-dropzone-addicon');
    }
});

Object.defineProperty(epfl.TypeAhead.prototype, 'remove_icon', {
    get: function () {
        return this.elm.find(".epfl-upload-remove-icon");
    }
});

epfl.Upload.prototype.handle_drag_over = function(e) {
        e.preventDefault();
        this.add_icon.hide();
        this.drop_zone.addClass('active');
};

epfl.Upload.prototype.handle_drag_leave = function(e) {
        e.preventDefault();
        this.add_icon.show();
        this.drop_zone.removeClass('active');
};

epfl.Upload.prototype.handle_drop = function(e) {
    //file drop event on drop zone, prevent default for no redirection to file
    var obj = this;
    e.preventDefault();

    //show the image and hide the plus icon
    obj.add_icon.hide();
    obj.image.show();
    obj.drop_zone.css({"border-color": "#D7D7D7"});

    //get the html tag of the dragged image
    var dataTransfer = $(e.dataTransfer.getData('text/html'));

    //extract src and check if the image is from a epfl compo
    var url = dataTransfer.attr("src");
    var droppedCid = dataTransfer.data("cid") || null;
    var isEpflUpload = dataTransfer.hasClass("epfl-upload-image");
    var isEpflImage = dataTransfer.hasClass("epfl-img-component-image");


    var type = null;
    //if the image has a url(src) its source is from the browser else the source is desktop
    if (url) {
        type = "extern";
        if (isEpflUpload) {
            type = "epfl_upload_image";
        }
        if (isEpflImage) {
            type = "epfl_image";
        }
        obj.image.attr('src', url);
        sendChange(url, type, droppedCid);
    } else {
        //load the desktop file to show it in the image tag
        var files = e.dataTransfer.files;
        type = "desktop";
        if (files.length) {

            if (!validateFile(files[0])) {
                return;
            }
            obj.reader.readAsDataURL(files[0]);
            obj.reader.onload = readerFinishedLoading;
        }
    }
};

epfl.Upload.prototype.handle_click = function (e) {
    epfl.ComponentBase.prototype.handle_click.call(this, e);
    if (obj.drop_zone.is(e.target)) {
        this.send_event('click', {});
    }
};

epfl.Upload.prototype.after_response = function(data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);

    var obj = this;

    var reader = new FileReader();
    obj.reader = reader;

    /**************************************************************************
     Helper Functions
     *************************************************************************/



    var validateFile = function (file) {
        var type_is_allowed = false;
        var i = 0;
        //check if file type is allowed
        if (obj.params.allowed_file_types) {
            if (file) {
                for (; i < obj.params.allowed_file_types.length; i++){
                    if(file.name.endsWith(obj.params.allowed_file_types[i])){
                        type_is_allowed = true;
                    }
                }
                if (!type_is_allowed){
                    alert("Unknown File Type");
                    return false;
                }
            }
        }
        if (file.size > parseInt(params["maximum_file_size"])) {
            alert("File size to big");
            return false;
        } else if (file.size > 200 * 1024 * 1024) {
            //200 MB is hard limit of upload compo
            alert("File size to big");
            return false;
        }
        return true;
    };
    //Send the change event
    var sendChange = function (value, type, droppedCid) {
        if (obj.params.fire_change_immediately) {
            epfl.send(epfl.make_component_event(cid, "change", {
                "value": value,
                "type": type,
                "dropped_cid": droppedCid
            }));
        } else {
            epfl.dispatch_event(cid, "change", {
                "value": value,
                "type": type,
                "dropped_cid": droppedCid
            })
        }
    };

    // called when the reader is finished sets the image in the container and fires change event
    var readerFinishedLoading = function () {
        if (obj.img_container.find('img').length !== 0) {
            obj.img_container.find('img').attr('src', reader.result);
        }
        sendChange(reader.result, "desktop", null)
    };

    /**************************************************************************
     Event Functions
     *************************************************************************/

    //fired when the fileinput changes
    var fileInputChange = function (event, data) {
        var file;
        //try get first file from data
        if (data && data.files && data.files.length) {
            file = data.files[0];
        }

        if (!file) {
            try {
                // Check if file was added with paste (only Chrome)
                items = event.clipboardData.items;
                var i = 0;
                for (; i < items.length; i++) {
                    file = items[i].getAsFile();
                    if (file) {
                        // It's a file that was pasted
                        break;
                    }
                }
            }
            catch (e) {
                // Change was triggered but there is no file, not selected by dialog, nor pasted via keyboard-commands,
                // but it is possible that items contains a single text string which would result in an error when
                // items[i].getAsFile() is executed on that string.
                return;
            }
        }

        if (!validateFile(file)) {
            return;
        }

        reader.readAsDataURL(file);
        reader.onload = readerFinishedLoading;
    };

    //Add File Event from file input
    var fileInputAdd = function (evt, data) {
        try {
            evt = evt.delegatedEvent.originalEvent;
        }
        catch (e) {
            //ignore errors and just return
            return;
        }
        fileInputChange(evt, data);
    };

    /**************************************************************************
     Event Handler
     *************************************************************************/

    //Drop Zone Events
    obj.drop_zone.on("dragover",  function (e) {
        obj.handle_drag_over(e);
    });
    obj.drop_zone.on("dragleave", function (e) {
        obj.handle_drag_leave(e);
    });
    obj.drop_zone.on('drop', function (e) {
        obj.handle_drop(e);
    });

    //File Input Events
    $(obj.input_selector).fileupload({
        add: fileInputAdd,
        dropZone: $("#" + cid + " div.epfl-upload-input-zone")
    });

    //Remove Icon Event
    if (obj.params.show_remove_icon) {
        var remove_icon = $("#" + cid + " .epfl-upload-remove-icon");
        if (remove_icon.length) {
            obj.remove_icon.click(function () {
                sendChange(null, null, null);
            });
        }
    }

};

// TODO: Remove this once ES6 is standard!
if (typeof String.prototype.endsWith !== 'function') {
    // Check if the given string ends with the given suffix.
    // As endsWith will (should) be implemented with ES6 this might get obsolete
    String.prototype.endsWith = function(suffix){
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    }
}
