from solute.epfl.components.form.inputbase import FormInputBase


class TextInput(FormInputBase):

    """
    A form text input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[TextInput(label="User name:", name="username")])

    """

    # general compo settings
    template_name = "text_input/text_input.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:text_input/static", "text_input.js"),
                                       ("solute.epfl.components:text_input/static",
                                        "jquery.datetimepicker.js"),
                                       ("solute.epfl.components:text_input/static", "bootstrap3-typeahead.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:text_input/static", "text_input.css"),
                                         ("solute.epfl.components:text_input/static", "jquery.datetimepicker.css")]
    new_style_compo = True
    compo_js_name = 'TextInput'
    compo_js_params = FormInputBase.compo_js_params + ['max_length', 'show_count', 'typeahead', 'type_func', 'date']
    compo_state = FormInputBase.compo_state + ['layover_icon']

    # derived attribute overrides
    validation_type = 'text'  #: Set the validation type, default 'text'

    # custom compo attributes
    typeahead = False  #: Set to true if typeahead should be provided by the input (if supported)
    type_func = 'typeahead'  #: Set the name of the function that is used to generate the typeahead values
    max_length = None  #: Maximum length for the input in characters
    show_count = False  #: Set to true to show a input counter right to the field. Requires a max_length to be set
    password = False  #: Set to true if input field should be used as a password field
    layover_icon = None  #: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
    date = False  #: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)

    def __init__(self, page, cid,
                 name=None,
                 default=None,
                 label=None,
                 mandatory=False,
                 value=False,
                 strip_value=False,
                 validation_error=None,
                 fire_change_immediately=False,
                 placeholder=None,
                 readonly=False,
                 submit_form_on_enter=False,
                 input_focus=False,
                 label_style=None,
                 input_style=None,
                 layout_vertical=None,
                 compo_col=12,
                 label_col=2,
                 validation_type=None,
                 typeahead=None,
                 type_func=None,
                 max_length=None,
                 show_count=None,
                 password=None,
                 layover_icon=None,
                 date=None,
                 **extra_params):
        """
        Form text input Component

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
        :param typeahead: Set to true if typeahead should be provided by the input (if supported)
        :param type_func: Set the name of the function that is used to generate the typeahead values
        :param max_length: Maximum length for the input in characters
        :param show_count: Set to true to show a input counter right to the field. Requires a max_length to be set
        :param password: Set to true if input field should be used as a password field
        :param layover_icon: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned
                             to the right)
        :param date: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
        """
        pass

    def handle_typeahead(self, query):
        pass
