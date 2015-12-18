epfl.TextEditor = function(cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.TextEditor.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.TextEditor.prototype, 'input_selector', {
    get: function() {
        return "#" + this.cid + "_texteditor";
    }
});

epfl.TextEditor.prototype.custom_handle_change = function(event) {
    // custom handler needed, cause the value is not just $elm.val()
    var value =  event.editor.getData();
    this.handle_change(event, value);
};

epfl.TextEditor.prototype.after_response = function(data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    var ed_config = this.params.editor_config_file + '.js';
    var clean_paste = this.params.clean_paste;
    clean_paste = (clean_paste === "True") ? true : false;

    var editor = CKEDITOR.replace(this.cid + "_texteditor", {
    	customConfig: ed_config,
    	forcePasteAsPlainText: clean_paste
    });

    editor.on('change', this.custom_handle_change.bind(this));
};
