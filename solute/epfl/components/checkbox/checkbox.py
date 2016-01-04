from solute.epfl.components.form.inputbase import FormInputBase


class Checkbox(FormInputBase):
    """
    A form checkbox input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Checkbox(label="I agree to the terms and conditions.", name="toc_agreed")])

    """

    # core internals
    template_name = "checkbox/checkbox.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:checkbox/static", "checkbox.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:checkbox/static", "checkbox.css")]

    # js settings
    compo_js_name = 'Checkbox'

    # derived attribute overrides
    validation_type = 'bool'  #: Validate this field as a boolean.

    # custom compo attributes

    #: If set to True, label and checkbox are not split to different bootstrap rows, but placed directly next to each
    #: other.
    compact = False
    #: If set to True, this checkbox belongs to a group of checkboxes where always just one can be checked.
    #: Note that to enable proper functionality of grouped option you have to set fire_change_immediately to True.
    grouped = False
    #: A list of checkbox-cids. If grouped is set to true, all cids in the group list will form a checkbox group
    #: where only one checkbox can be checked at a time.
    group = []

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
                 compact=None,
                 grouped=None,
                 group=None, **extra_params):
        """Checkbox component

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
        :param compact: (bool, optional) place label and checkbox directly to each other
        :param grouped: (bool, optional) Used to distinct if a checkbox is part of a group.
        :param group: (list, optional) A list of cids, describing which checkboxes are part of this checkbox group.
        """
        pass

    def handle_change(self, value):
        self.value = value
        if not self.grouped and len(self.group) > 0:
            # for grouped checkboxes the group has to contain at least 1 other checkbox
            return
        group = self.group
        if value is True:
            for chbox in group:
                check_box = getattr(self.page, chbox)
                check_box.handle_change(False)
        self.redraw()
