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
    js_parts = []
    js_name = FormInputBase.js_name + [("solute.epfl.components:number_input/static", "number_input.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:number_input/static", "number_input.css")]
    new_style_compo = True
    compo_js_name = 'NumberInput'
    compo_state = FormInputBase.compo_state + ['min_value', 'max_value']

    #: Possible values are 'float' and 'number' (which is default). If set to 'float' a text-input will be displayed
    #: that takes only numbers and a '.' or ',' as a separator.
    validation_type = 'number'
    layout_vertical = False  #: Display vertical instead of horizontal layout.
    min_value = None  #: If set, the minimum value to be supported by the control.
    max_value = None  #: If set, the maximum value to be supported by the control.
    input_pattern = None  #: If set, used as HTML 5 pattern for immediate validation of the input field

    def __init__(self, page, cid, label=None, name=None, min_value=None, max_value=None, input_pattern=None,
                 default=None, validation_type=None, **extra_params):
        '''
        NumberInput Component

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
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
