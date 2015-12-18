from solute.epfl.components.form.inputbase import FormInputBase


class Textarea(FormInputBase):
    """
    A form multi-line text area

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Textarea(label="Provide a description:", name="description")])

    """
    template_name = "textarea/textarea.html"
    js_parts = []
    js_name = FormInputBase.js_name + [("solute.epfl.components:textarea/static", "textarea.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:textarea/static", "textarea.css")]

    new_style_compo = True
    compo_js_name = 'Textarea'

    validation_type = 'text'  #: Validate component as text.

    def __init__(self, page, cid, **extra_params):
        """Simple Textarea form input.
        """
        super(Textarea, self).__init__(page, cid, **extra_params)
