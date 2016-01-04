from solute.epfl.components.form.inputbase import FormInputBase


class SimpleToggle(FormInputBase):
    """
    A form checkbox styled as a simple on/off toggle.
    Compared to the Toggle component, this component does not display any texts on the toggle.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[SimpleToggle(label="Enable/Disable user:", name="user_enable_toggle")])

    """

    template_name = "simpletoggle/simpletoggle.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:simpletoggle/static", "simpletoggle.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:simpletoggle/static", "simpletoggle.css")]
    compo_js_name = 'SimpleToggle'
    compo_js_params = FormInputBase.compo_js_params + ['enabled_icon', "disabled_icon", "enabled_icon_size",
                                                       "disabled_icon_size", "enabled_icon_color",
                                                       "disabled_icon_color"]
    compo_js_extras = ['handle_click']
    compo_state = FormInputBase.compo_state + [
        "enabled_icon", "disabled_icon", "enabled_icon_size", "disabled_icon_size", "enabled_icon_color",
        "disabled_icon_color"]

    # derived attribute overrides
    validation_type = 'bool'  #: Form validation selector.
    default = False  #: The default value of the toggle.

    # custom compo attributes
    enabled_icon = "toggle-on"  #: font-awesome icon to be rendered if value == True
    disabled_icon = "toggle-off"  #: font-awesome icon to be rendered if value == False
    enabled_icon_size = "lg"  #: font-awesome icon size if value == True example lg,2x,3x etc
    disabled_icon_size = "lg"  #: font-awesome icon size if value == False  lg,2x,3x ect
    enabled_icon_color = "primary"  #: bootstrap color if value == True example: primary default warning etc
    disabled_icon_color = "default"  #: bootstrap color if value == False example: primary default warning etc

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
                 enabled_icon=None,
                 disabled_icon=None,
                 enabled_icon_size=None,
                 disabled_icon_size=None,
                 enabled_icon_color=None,
                 disabled_icon_color=None,
                 **extra_params):
        """
        Form simple toggle Component

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
        :param enabled_icon: font-awesome icon to be renderd if value == True
        :param disabled_icon: font-awesome icon to be renderd if value == False
        :param enabled_icon_size: font-awesome icon size if value == True example lg,2x,3x etc
        :param disabled_icon_size: font-awesome icon size if value == False  lg,2x,3x etc
        :param enabled_icon_color: bootstrap color if value == True example: primary default warning etc
        :param disabled_icon_color: bootstrap color if value == False example: primary default warning etc
        :return:
        """
        pass
