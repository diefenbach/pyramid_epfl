from solute.epfl.components.form.inputbase import FormInputBase


class ButtonRadio(FormInputBase):
    """
    A form radio group using buttons as radio fields.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[ButtonRadio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """

    # core internals
    template_name = "buttonradio/buttonradio.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:buttonradio/static", "buttonradio.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:buttonradio/static", "buttonradio.css")]
    compo_state = FormInputBase.compo_state + ['options']

    # js settings
    compo_js_name = 'ButtonRadio'

    # derived attribute overrides
    validation_type = 'text'  #: Evaluate this component as text.

    # custom compo attributes
    options = ""  #: List of strings or key, value tuples presented as options.

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
                 options=None,
                 **extra_params):
        """A component displaying a radio form input with buttons.

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
        :param options: List of strings or key, value tuples presented as options.
        """
        pass
