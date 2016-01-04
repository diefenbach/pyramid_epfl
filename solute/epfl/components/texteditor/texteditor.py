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

    # derived attribute overrides
    validation_type = 'text'  #: Validate this component as text.

    # custom compo attributes

    #: The config-file that should be used for this instance. Available are at least "config" and "slimconfig"
    editor_config_file = "config"
    #: Set True to automatically remove all formatting on paste
    clean_paste = False

    def __init__(self, page, cid,
                 name=None,
                 default=None,
                 label=None,
                 mandatory=None,
                 value=None,
                 strip_value=None,
                 validation_error=None,
                 fire_change_immediately=None,
                 placeholder=None,
                 readonly=None,
                 submit_form_on_enter=None,
                 input_focus=None,
                 label_style=None,
                 input_style=None,
                 layout_vertical=None,
                 compo_col=None,
                 label_col=None,
                 validation_type=None,
                 editor_config_file=None,
                 clean_paste=None,
                 **extra_params):
        """A wysiwyg text editor.

        :param name: An element without a name cannot have a value
        :param default: Default value that may be pre-set or pre-selected
        :param label: Optional label describing the input field
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param value: The actual value of the input element that is posted upon form submission
        :param strip_value: strip value if True in get value
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server.
                                        Otherwise, change events are fired upon the next immediate epfl event
        :param placeholder: Placeholder text that can be displayed if supported by the input
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param submit_form_on_enter: If true, underlying form is submitted upon enter key in this input
        :param input_focus: Set focus on this input when component is displayed
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before
                                it
        :param compo_col: Set the width of the complete input component (default: max: 12)
        :param label_col: Set the width of the complete input component (default: 2)
        :param validation_type: Set the validation type, default 'text'
        :param editor_config_file: Config to be used can be either the default "config" or "slimconfig".
        :param clean_paste: Automatically remove all formatting on paste.
        """
        pass
