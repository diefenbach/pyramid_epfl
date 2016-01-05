from solute.epfl.core.epflcomponentbase import ComponentBase


class FormInputBase(ComponentBase):
    """ A base class for input/form based components. """

    # general compo settings
    asset_spec = "solute.epfl.components:form/static"
    js_name = ["input_base.js"]
    css_name = ["input_base.css"]
    compo_js_auto_parts = True
    compo_js_name = 'FormInputBase'
    compo_js_params = ['submit_form_on_enter', 'input_focus', 'fire_change_immediately', 'label_style', 'input_style']
    compo_state = ['label', 'readonly']

    # custom compo attributes
    label = None  #: Optional label describing the input field.
    fire_change_immediately = False
    placeholder = None  #: Placeholder text that can be displayed if supported by the input.
    readonly = False
    submit_form_on_enter = False  #: If true, underlying form is submitted upon enter key in this input
    input_focus = False  #: Set focus on this input when component is displayed
    label_style = None
    input_style = None
    layout_vertical = False
    compo_col = 12
    label_col = 2

    def init_transaction(self):
        super(FormInputBase, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default

    def set_focus(self):
        self.add_js_response("setTimeout(function(){$('#%s_input').focus(); }, 0);" % self.cid)
        self.redraw()
