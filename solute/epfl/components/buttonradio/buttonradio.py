from solute.epfl.components.form.inputbase import FormInputBase


class ButtonRadio(FormInputBase):
    """
    A form radio group using buttons as radio fields.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[ButtonRadio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """

    template_name = "buttonradio/buttonradio.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:buttonradio/static", "buttonradio.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:buttonradio/static", "buttonradio.css")]
    compo_js_name = 'ButtonRadio'
    compo_state = FormInputBase.compo_state + ['options']

    options = ""  #: List of strings or key, value tuples presented as options.
    validation_type = 'text'  #: Evaluate this component as text.

    def __init__(self, page, cid, options=None, **extra_params):
        """A component displaying a radio form input with buttons.

        :param options: List of strings or key, value tuples presented as options.
        """
        pass
