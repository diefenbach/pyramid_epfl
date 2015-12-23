from solute.epfl.components.form.inputbase import FormInputBase


class TextEditor(FormInputBase):
    """
    A form wysiwyg text editor supporting BBCode.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[TextEditor(label="Provide a description:", name="description")])

    """

    template_name = "texteditor/texteditor.html"
    js_name = [('solute.epfl.components:texteditor/static', 'texteditor.js')]
    js_name_no_bundle = [('solute.epfl.components:texteditor/static', 'ckeditor.js')]
    compo_js_name = 'TextEditor'
    compo_js_params = ['editor_config_file', 'clean_paste']

    validation_type = 'text'  #: Validate this component as text.
    #: The config-file that should be used for this instance. Available are at least "config" and "slimconfig"
    editor_config_file = "config"
    #: Set True to automatically remove all formatting on paste
    clean_paste = False

    def __init__(self, page, cid, editor_config_file=None, clean_paste=None, **extra_params):
        """A wysiwyg text editor.

        :param editor_config_file: Config to be used can be either the default "config" or "slimconfig".
        :param clean_paste: Automatically remove all formatting on paste.
        """
        pass
