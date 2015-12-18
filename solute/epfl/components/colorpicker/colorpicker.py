# * encoding: utf-8

from solute.epfl.components.form.inputbase import FormInputBase


class ColorPicker(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorpicker/static", "colorpicker.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorpicker/static", "colorpicker.css")]
    template_name = "colorpicker/colorpicker.html"
    compo_state = FormInputBase.compo_state + ["value_options", "toggle_button", "colors_visible"]
    js_parts = []

    TYPE_RGB = 0  #: Constant for value options list, show data as rgb

    TYPE_SPECIAL = 1  #: Constant for value options list, show data as special

    value_options = None  #: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}

    toggle_button = False  #: Show a toggle button for the colors

    colors_visible = False  #: Works only with toggle button, set colors visible

    new_style_compo = True
    compo_js_params = FormInputBase.compo_js_params + ['colors_visible']
    compo_js_name = 'ColorPicker'
    compo_js_extras = ['handle_click']

    def __init__(self, page, cid, value_options=None, toggle_button=None, colors_visible=None, **extra_params):
        """ColorPicker compo displays a selectable list of colors, or special values such as transparent

        :param value_options: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}
        :param toggle_button: Show a toggle button for the colors
        :param colors_visible: Works only with toggle button, set colors visible
        """
        super(ColorPicker, self).__init__(page=page, cid=cid, value_options=value_options, toggle_button=toggle_button,
                                          colors_visible=colors_visible, **extra_params)

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
