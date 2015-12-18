from solute.epfl.core.epflcomponentbase import ComponentBase
from form import Form


class FormInputBase(ComponentBase):
    asset_spec = "solute.epfl.components:form/static"

    compo_state = ['label', 'readonly']
    #js_parts = ["form/input_base.js"]
    js_parts = []

    js_name = ["input_base.js"]
    css_name = ["input_base.css"]

    label = None  #: Optional label describing the input field.
    default = None  #: Default value that may be pre-set or pre-selected
    placeholder = None  #: Placeholder text that can be displayed if supported by the input.
    readonly = False

    submit_form_on_enter = False  #: If true, underlying form is submitted upon enter key in this input
    input_focus = False  #: Set focus on this input when component is displayed

    #: Set to true if input change events should be fired immediately to the server.
    #: Otherwise, change events are fired upon the next immediate epfl event.
    fire_change_immediately = False

    compo_col = 12
    label_col = 2
    layout_vertical = False
    label_style = None
    input_style = None

    new_style_compo = True
    compo_js_name = 'FormInputBase'
    compo_js_params = ['submit_form_on_enter', 'input_focus', 'fire_change_immediately', 'label_style', 'input_style']
    compo_js_extras = []

    def __init__(self, page, cid, label=None, name=None, default="", validation_type="",
                 **extra_params):
        super(FormInputBase, self).__init__()

    def init_transaction(self):
        super(FormInputBase, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default

    def set_focus(self):
        self.add_js_response("setTimeout(function(){$('#%s_input').focus(); }, 0);" % self.cid)
        self.redraw()
