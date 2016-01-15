epfl.CodeEditor = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};
epfl.CodeEditor.inherits_from(epfl.FormInputBase);


Object.defineProperty(epfl.CodeEditor.prototype, 'textarea', {
    get: function () {
        return this.elm.find('textarea');
    }
});

epfl.CodeEditor.prototype.handle_changes = function (event, changes) {
    var evt = this.make_event('change', {value: this.code_mirror.doc.getValue()});
    epfl.repeat_enqueue(evt, this.cid + "_change");
};

epfl.CodeEditor.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);
    this.code_mirror = CodeMirror.fromTextArea(this.textarea[0], {
        mode: this.params.language_mode
    });

    var obj = this;
    this.code_mirror.on('changes', function (e, changes) {
        obj.handle_changes(e, changes);
    });
    this.code_mirror.setSize('100%', '100%');
};
