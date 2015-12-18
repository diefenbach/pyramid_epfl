from solute.epfl.components.form.inputbase import FormInputBase


class Toggle(FormInputBase):
    """
    A form checkbox styled as toggle.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Toggle(label="Enable/Disable user:", name="user_enable_toggle")])

    """

    template_name = "toggle/toggle.html"
    js_parts = []
    js_name = FormInputBase.js_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.js"),
                                       ("solute.epfl.components:toggle/static", "toggle.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.css"),
                                         ("solute.epfl.components:toggle/static", "toggle.css")]

    validation_type = 'bool'  #: Validate this component as a boolean.

    on_text = "on"  #: The text to be displayed if toggle is set to on.
    off_text = "off"  #: The text to be displayed if toggle is set to off.
    default = False  #: The default value of the toggle.

    new_style_compo = True
    compo_js_name = 'Toggle'

    def __init__(self, page, cid, on_text=None, off_text=None, default=None, **extra_params):
        """A toggling form input.

        :param on_text: Text shown for the "on" state evaluating to a value of True.
        :param off_text: Text shown for the "off" state evaluating to a value of False.
        :param default: Initial value the component will hold.
        """
        super(Toggle, self).__init__(page, cid, on_text=on_text, off_text=off_text, default=default, **extra_params)
