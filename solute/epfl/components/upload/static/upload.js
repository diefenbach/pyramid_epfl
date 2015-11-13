epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Upload.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Upload.prototype, 'remove_icon', {
    get: function () {
        return this.elm.find('.epfl-upload-remove-icon');
    }
});

Object.defineProperty(epfl.Upload.prototype, 'dropzone', {
    get: function () {
        return this.elm.find(".epfl-dropzone");
    }
});

epfl.Upload.prototype.is_async_uploading = false;

epfl.Upload.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    var obj = this;
    if (obj.params['show_file_upload_input']) {
        obj.elm.find("input").fileupload({
            add: obj.file_input_add.bind(obj),
            dropZone: null //drag and drop is handled by epfl, this must be null to prevent double events
        });
    }

    //if not remove icon is shown and the value is not null the dragover dragleave and drop event
    //should do nothing except prevent default
    if (obj.params["show_remove_icon"] === true && obj.params["value"] != null) {
        obj.elm.off("dragover").off("dragleave").off("drop");
        obj.elm.on('dragover', function (event) {
            event.preventDefault();
            return true;
        }).on('drop', function (event) {
            event.preventDefault();
        });
    }
};

epfl.Upload.prototype.file_input_add = function (evt, data) {
    var obj = this;
    try {
        evt = evt.delegatedEvent.originalEvent;
    }
    catch (e) {
        //ignore errors and just return
        return;
    }

    var files;
    //try get first file from data
    if (data && data.files && data.files.length) {
        files = data.files;
    }

    if (!files) {
        files = [];
        try {
            // Check if file was added with paste (only Chrome)
            items = event.clipboardData.items;
            var i = 0;
            for (; i < items.length; i++) {
                var file = items[i].getAsFile();
                if (file) {
                    // It's a file that was pasted
                    files.push(file);
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

    if (files) {
        obj.handle_drop_file(files, evt);
    }
};

epfl.Upload.prototype.validate_files = function (data) {
    //validate all files in data, data need the format from epfl.Upload.prototype.extract_file_data
    var obj = this;

    for (var i = 0; i < data.length; i++) {
        //check file type
        try {
            if (obj.params.allowed_file_types) {
                var type_is_allowed = false;
                for (var j = 0; j < obj.params.allowed_file_types.length; j++) {
                    if (data[i].name.toLowerCase().endsWith(obj.params.allowed_file_types[j].toLowerCase())) {
                        type_is_allowed = true;
                    }
                }
                if (!type_is_allowed) {
                    epfl.show_message({
                        msg: data[i].name + ": " + obj.params["error_message_file_type"],
                        typ: "warning", "fading": true
                    });
                    data[i].valid = false;
                    continue;
                }
            }

            //check file size
            if (data[i].file_size > parseInt(obj.params.maximum_file_size)) {
                epfl.show_message({
                    msg: data[i].name + ": " + obj.params["error_message_file_size"],
                    typ: "warning", "fading": true
                });
                data[i].valid = false;
                continue;
            } else if (data[i].file_size > 200 * 1024 * 1024) {
                //200 MB is hard limit of upload compo
                epfl.show_message({
                    msg: data[i].name + ": " + obj.params["error_message_file_size"],
                    typ: "warning", "fading": true
                });
                data[i].valid = false;
                continue;
            }

            //check image max width
            if (obj.params["maximum_image_width"] && data[i].file_is_img) {
                if (data[i].file_img_width > obj.params["maximum_image_width"]) {
                    epfl.show_message({
                        msg: data[i].name + ": " + obj.params["error_message_image_size_to_big"],
                        typ: "warning", "fading": true
                    });
                    data[i].valid = false;
                    continue;
                }
            }

            //check image max height
            if (obj.params["maximum_image_height"] && data[i].file_is_img) {
                if (data[i].file_img_height > obj.params["maximum_image_height"]) {
                    epfl.show_message({
                        msg: data[i].name + ": " + obj.params["error_message_image_size_to_big"],
                        typ: "warning", "fading": true
                    });
                    data[i].valid = false;
                    continue;
                }
            }

            //check image min width
            if (obj.params["minimum_image_width"] && data[i].file_is_img) {
                if (data[i].file_img_width < obj.params["minimum_image_width"]) {
                    epfl.show_message({
                        msg: data[i].name + ": " + obj.params["error_message_image_size_to_small"],
                        typ: "warning", "fading": true
                    });
                    data[i].valid = false;
                    continue;
                }
            }

            //check image min height
            if (obj.params["minimum_image_height"] && data[i].file_is_img) {
                if (data[i].file_img_height < obj.params["minimum_image_height"]) {
                    epfl.show_message({
                        msg: data[i].name + ": " + obj.params["error_message_image_size_to_small"],
                        typ: "warning", "fading": true
                    });
                    data[i].valid = false;
                    continue;
                }
            }
        } catch (e) {
            console.log("Upload: Exception while validation", e);
            data[i].valid = false;
            continue;
        }
        data[i].valid = true;
    }
    return data;
};


epfl.Upload.prototype.addSpinner = function () {
    var spinner = $("<div class='text-center text-primary epfl-upload-loading-indicator'><i class='fa fa-cog fa-5x fa-spin'></i></div>");
    spinner.appendTo(this.elm);
};

epfl.Upload.prototype.removeSpinner = function () {
    var spinner = this.elm.find(".epfl-upload-loading-indicator");
    spinner.remove();
};


epfl.Upload.prototype.upload_files_async = function (data) {
    //upload all valid files in data async, data need the format from epfl.Upload.prototype.extract_file_data
    var obj = this;
    obj.is_async_uploading = true;
    var raw_files = [];
    for (var i = 0; i < data.length; i++) {
        if (!data[i].valid) {
            continue;
        }
        raw_files.push({data: data[i].reader_result, name: data[i].file_name});
    }

    obj.send_async_event('store', {files: raw_files}, function (data) {
        obj.is_async_uploading = false;
        //TODO: make result visible
        obj.handle_drop_url(data);
    });
};


epfl.Upload.prototype.upload_files_sync = function (data) {
    //normal sync upload, data need the format from epfl.Upload.prototype.extract_file_data
    var obj = this;
    var raw_files = [];
    for (var i = 0; i < data.length; i++) {
        if (!data[i].valid) {
            continue;
        }
        raw_files.push({data: data[i].reader_result, name: data[i].file_name});
    }
    obj.change(raw_files)
};

epfl.Upload.prototype.check_for_valid_files = function (data) {
    //check if any entry in data is valid, data need the format from epfl.Upload.prototype.extract_file_data
    for (var i = 0; i < data.length; i++) {
        if (data[i].valid) {
            return true;
        }
    }
    return false;
};

epfl.Upload.prototype.send_file_infos = function (data) {
    //send the file info of all valid files in data, data need the format from epfl.Upload.prototype.extract_file_data
    var obj = this;
    var file_infos = [];
    for (var i = 0; i < data.length; i++) {
        if (!data[i].valid) {
            continue;
        }
        file_infos.push({
            size: data[i].file_size,
            type: data[i].file_type,
            name: data[i].file_name,
            is_image: data[i].file_is_img,
            image_width: data[i].file_img_width,
            image_height: data[i].file_img_height
        });
    }

    obj.send_event('file_info', {file_infos: file_infos});
};


epfl.Upload.prototype.handle_drop_file = function (files, event) {
    var obj = this;

    // Currently only single files supported, although that's really only a question of implementing a backend.
    obj.dropzone.hide();
    obj.addSpinner();

    obj.extract_file_data(files, function (file_data) {
        file_data = obj.validate_files(file_data);
        if (!obj.check_for_valid_files(file_data)) {
            //no valid files
            obj.dropzone.show();
            obj.removeSpinner();
            return;
        }

        obj.send_file_infos(file_data);
        if (obj.params["store_async"]) {
            obj.upload_files_async(file_data);
        } else {
            obj.upload_files_sync(file_data);
        }
    });
};


epfl.Upload.prototype.extract_file_data = function (files, callback) {
    //read all files extract their data and call next functions
    var file_data = [];
    var files_read = 0;
    for (var i = 0; i < files.length; i++) {
        var reader = new FileReader();
        reader.onload = (function (file) {
            return function () {
                var that = this;
                var img = new Image();
                img.src = this.result;

                var imageLoaded = function (error) {
                    file_data.push({
                        name: file.name,
                        reader_result: that.result,
                        file_size: file.size,
                        file_name: file.name,
                        file_type: file.name.split('.').pop(),
                        file_is_img: !error,
                        file_img_width: error ? null : img.width,
                        file_img_height: error ? null : img.height,
                        valid: false
                    });
                    files_read += 1;

                    //if all files are successfull read and their data are extracted go on
                    if (files_read === files.length) {
                        callback(file_data);
                    }
                };

                img.onload = function () {
                    imageLoaded(false);
                };

                img.onerror = function () {
                    imageLoaded(true);
                };
            }
        })(files[i]);
        reader.readAsDataURL(files[i]);
    }
};


epfl.Upload.prototype.handle_drop_url = function (url, event) {
    this.change(url);
};

epfl.Upload.prototype.change = function (value) {
    this.removeSpinner();
    var enqueue_event = true;
    if (this.params.fire_change_immediately) {
        enqueue_event = false;
    }
    var parent_form = this.elm.closest('.epfl-form');
    if (parent_form.length == 1) {
        var is_dirty = parent_form.data('dirty');
        if (is_dirty == '0') {
            parent_form.data('dirty', '1');
            // first change to the form. always send event immediately so that
            // the serve can handle is_dirty change
            enqueue_event = false;

            this.repeat_enqueue('set_dirty', {}, this.cid + "_set_dirty");
        }
    }
    if (enqueue_event) {
        this.repeat_enqueue('change', {value: value}, this.cid + "_change");
    } else {
        this.send_event('change', {value: value});
    }
};

epfl.Upload.prototype.handle_click = function (event) {
    if (this.is_async_uploading) {
        return;
    }
    epfl.ComponentBase.prototype.handle_click.call(this, event);

    if (this.remove_icon.is(event.target)) {
        this.send_event('remove_icon', {});
    } else if (this.params.handle_click) {
        this.send_event('click', {});
    }
};

