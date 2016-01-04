from solute.epfl.components.form.inputbase import FormInputBase
from solute.epfl.core import epflvalidators


class NumberInput(FormInputBase):
    """
    A form number input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[NumberInput(label="Age:", name="age")])

    """

    template_name = "number_input/number_input.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:number_input/static", "number_input.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:number_input/static", "number_input.css")]
    compo_js_name = 'NumberInput'
    compo_state = FormInputBase.compo_state + ['min_value', 'max_value']

    # derived attribute overrides

    #: Possible values are 'float' and 'number' (which is default). If set to 'float' a text-input will be displayed
    #: that takes only numbers and a '.' or ',' as a separator.
    validation_type = 'number'
    layout_vertical = False  #: Display vertical instead of horizontal layout.

    # custom compo attributes
    min_value = None  #: If set, the minimum value to be supported by the control.
    max_value = None  #: If set, the maximum value to be supported by the control.
    input_pattern = None  #: If set, used as HTML 5 pattern for immediate validation of the input field

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
                 min_value=None,
                 max_value=None,
                 input_pattern=None,
                 **extra_params):
        '''
        NumberInput Component

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
        :param min_value: The minimum value that can be set to this field
        :param max_value: The maximum value that can be set to this field
        :param input_pattern: HTML 5 pattern to be used for the input field for immediate field validation
        '''
        pass

    def init_transaction(self):
        """ Calling super().init_transaction extended with default validators for
        min_value and max_value.
        """
        super(NumberInput, self).init_transaction()

        if self.name and self.validation_type == 'number' and \
           (getattr(self, 'min_value', None) is not None or
            getattr(self, 'max_value', None) is not None):
            number_validator = epflvalidators.ValidatorBase.by_name('number')(min_value=self.min_value,
                                                                              max_value=self.max_value)
            self.validators.insert(0, number_validator)

    def handle_change(self, value):
        if self.validation_type == 'float' and value is not None:
            try:
                value = float(str(value).replace(",", "."))
            except ValueError:
                value = None
        self.value = value
