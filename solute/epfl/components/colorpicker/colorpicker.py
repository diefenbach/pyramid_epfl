# * encoding: utf-8

from solute.epfl.components.form.inputbase import FormInputBase


class ColorPicker(FormInputBase):

    template_name = "colorpicker/colorpicker.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorpicker/static", "colorpicker.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorpicker/static", "colorpicker.css")]
    compo_js_params = FormInputBase.compo_js_params + ['colors_visible']
    compo_js_name = 'ColorPicker'
    compo_js_extras = ['handle_click']
    compo_state = FormInputBase.compo_state + ["value_options", "toggle_button", "colors_visible"]

    TYPE_RGB = 0  #: Constant for value options list, show data as rgb
    TYPE_SPECIAL = 1  #: Constant for value options list, show data as special

    # custom compo attributes
    value_options = None  #: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}
    toggle_button = False  #: Show a toggle button for the colors
    colors_visible = False  #: Works only with toggle button, set colors visible

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
                 value_options=None,
                 toggle_button=None,
                 colors_visible=None,
                 **extra_params):
        """ColorPicker compo displays a selectable list of colors, or special values such as transparent

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
        :param value_options: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}
        :param toggle_button: Show a toggle button for the colors
        :param colors_visible: Works only with toggle button, set colors visible
        """
        pass

    def handle_change(self, value):
        if self.value is None:
            self.value = []

        # check if value is in self value if true remove else add
        full_value = next((val for val in self.value_options if val["data"] == value), None)
        if full_value in self.value:
            self.value.remove(full_value)
        else:
            self.value.append(full_value)
        self.redraw()

    def handle_toggle(self):
        self.colors_visible = not self.colors_visible
        self.redraw()
