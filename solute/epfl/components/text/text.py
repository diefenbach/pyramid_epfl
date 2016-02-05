from solute.epfl.core import epflcomponentbase


class Text(epflcomponentbase.ComponentBase):

    # general compo settings
    asset_spec = "solute.epfl.components:text/static"
    css_name = ["text.css"]
    template_name = "text/text.html"
    compo_state = epflcomponentbase.ComponentBase.compo_state + ["value", "tag", "tag_class", "label"]

    # custom compo attributes
    value = None  #: The textual value of this component.
    tag = None  #: HTML tag to use as container for the text.
    tag_class = None  #: css class to use on the container of the text.
    label = None  #: Label to be used for this text component.
    title = None  #: Set the title attribute of the element
    layout_vertical = False  #: Set to True if label should be displayed on top of the compo and not on the left before it
    label_col = 2  #: Set the width of the label of the component (default: 2, max: 12)
    compo_col = 12  #: Set the width of the complete component (default: 12, max: 12)
    label_style = None  #: Can be used to add additional css styles for the label

    def __init__(self, page, cid,
                 value=None,
                 tag=None,
                 tag_class=None,
                 title=None,
                 label=None,
                 layout_vertical=None,
                 label_col=None,
                 **extra_params):
        """A very basic component to display text values.

        :param value: The textual value of this component.
        :param tag: HTML tag to use as container for the text.
        :param tag_class: css class to use on the container of the text.
        :param title: Set the title attribute of the element.
        :param label: Label to be used for this text component.
        :param layout_vertical: Set to True if label should be displayed on top of the compo and not on the left before it
        :param label_col: Set the width of the label of the component (default: 2, max: 12)
        :param compo_col: Set the width of the complete component (default: 12, max: 12)
        :param label_style: Can be used to add additional css styles for the label
        """
        pass
