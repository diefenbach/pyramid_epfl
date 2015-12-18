from solute.epfl.components.form.inputbase import FormInputBase


class TextInput(FormInputBase):

    """
    A form text input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[TextInput(label="User name:", name="username")])

    """

    template_name = "text_input/text_input.html"
    js_parts = []
    js_name = FormInputBase.js_name + [("solute.epfl.components:text_input/static", "text_input.js"),
                                       ("solute.epfl.components:text_input/static",
                                        "jquery.datetimepicker.js"),
                                       ("solute.epfl.components:text_input/static", "bootstrap3-typeahead.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:text_input/static", "text_input.css"),
                                         ("solute.epfl.components:text_input/static", "jquery.datetimepicker.css")]

    compo_state = FormInputBase.compo_state + ['layover_icon']

    #: Maximum length for the input
    max_length = None

    #: Set to true to show a input counter right to the field. Requires a max_length to be set.
    show_count = False

    validation_type = 'text'  #: Validate as text.

    #: Set to true if typeahead should be provided by the input (if supported)
    typeahead = False

    #: Set the name of the function that is used to generate the typeahead values
    type_func = 'typeahead'

    #: Set to true if input field should be used as a password field
    password = False

    #: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
    layover_icon = None

    #: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
    date = False

    #: A text input always submits the form if enter is pressed. Hence, this field is not needed and False by default
    submit_form_on_enter = False

    new_style_compo = True
    compo_js_params = FormInputBase.compo_js_params + ['max_length', 'show_count', 'typeahead', 'type_func', 'date']
    compo_js_name = 'TextInput'

    def __init__(self, page, cid,
                 label=None,
                 name=None,
                 value=None,
                 default=None,
                 placeholder=None,
                 readonly=None,
                 validation_error=None,
                 mandatory=None,
                 input_focus=False,
                 fire_change_immediately=None,
                 compo_col=None,
                 label_col=None,
                 layout_vertical=None,
                 label_style=None,
                 input_style=None,
                 typeahead=None,
                 max_length=None,
                 show_count=None,
                 password=None,
                 layover_icon=None,
                 date=None,
                 **extra_params):
        """
        Form text input Component

        :param label: Optional label describing the input field
        :param name: An element without a name cannot have a value
        :param value: The actual value of the input element that is posted upon form submission
        :param default: Default value that may be pre-set or pre-selected
        :param placeholder: Placeholder text that can be displayed if supported by the input
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param input_focus: Set focus on this input when component is displayed
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server. Otherwise, change events are fired upon the next immediate epfl event
        :param compo_col: Set the width of the complete input component (default: max: 12)
        :param label_col: Set the width of the complete input component (default: 2)
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before it
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        :param typeahead: Set to true if typeahead should be provided by the input (if supported)
        :param max_length: Maximum length for the input
        :param show_count: Set to true to show a input counter right to the field. Requires a max_length to be set
        :param password: Set to true if input field should be used as a password field
        :param layover_icon: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
        :param date: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
        """
        super(TextInput, self).__init__(page, cid,
                                        label=label,
                                        name=name,
                                        value=value,
                                        default=default,
                                        placeholder=placeholder,
                                        readonly=readonly,
                                        validation_error=validation_error,
                                        mandatory=mandatory,
                                        input_focus=input_focus,
                                        fire_change_immediately=fire_change_immediately,
                                        compo_col=compo_col,
                                        label_col=label_col,
                                        layout_vertical=layout_vertical,
                                        label_style=label_style,
                                        input_style=input_style,
                                        typeahead=typeahead,
                                        max_length=max_length,
                                        show_count=show_count,
                                        password=password,
                                        layover_icon=layover_icon,
                                        **extra_params)

    def handle_typeahead(self, query):
        pass
