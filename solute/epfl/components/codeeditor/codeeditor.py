from solute.epfl.components.form.inputbase import FormInputBase


class CodeEditor(FormInputBase):
    """
    A form wysiwyg text editor supporting BBCode.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[TextEditor(label="Provide a description:", name="description")])
    
    """
    js_parts = []
    js_name = [('solute.epfl.components:codeeditor/static', 'codeeditor.js')]
    js_name_no_bundle = [
        ('solute.epfl.components:codeeditor/static', 'codemirror/lib/codemirror.js'),
    ]
    css_name = [('solute.epfl.components:codeeditor/static', 'codemirror/lib/codemirror.css')]

    template_name = "codeeditor/codeeditor.html"

    validation_type = 'text'  #: Validate this component as text.

    new_style_compo = True
    compo_js_name = 'CodeEditor'

    def __init__(self, page, cid, **extra_params):
        """A code editor.

        :param editor_config_file: Config to be used can be either the default "config" or "slimconfig".
        :param clean_paste: Automatically remove all formatting on paste.
        """
        super(CodeEditor, self).__init__(page, cid, **extra_params)
