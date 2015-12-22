epfl.TextEditor = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.TextEditor.inherits_from(epfl.ComponentBase);

epfl.TextEditor.prototype.handle_change = function(event) {
    epfl.repeat_enqueue(epfl.make_component_event(this.cid, 'change', {value:  event.editor.getData()}), this.cid + "_change");
};

epfl.TextEditor.prototype.after_response = function(data) {
    var compo = this;
    var selector = "#" + this.cid + "_texteditor";
    var ed_config = this.params.editor_config_file + '.js';
    var clean_paste = this.params.clean_paste;
    clean_paste = (clean_paste === "True") ? true : false;

    var editor = CKEDITOR.replace(this.cid + "_texteditor", {
    	customConfig: ed_config,
    	forcePasteAsPlainText: clean_paste
    });

    editor.on('change', this.handle_change.bind(this));
};
